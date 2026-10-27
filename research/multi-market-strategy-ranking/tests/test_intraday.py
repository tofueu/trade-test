"""Offline tests for real intraday loader and strict qualification (no network)."""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
spec = importlib.util.spec_from_file_location("run_intraday", SRC / "run_intraday.py")
intraday = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intraday)


def zip_csv(csv_text):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("BTCUSDT-1h-sample.csv", csv_text)
    return buffer.getvalue()


class IntradayTests(unittest.TestCase):
    def test_real_zip_parsing_ms_and_microseconds(self):
        for multiplier in (1000, 1000000):
            ts = 1633824000 * multiplier
            payload = zip_csv(
                "open_time,open,high,low,close,volume\n"
                f"{ts},100,110,90,105,123\n"
                f"{ts + 3600 * multiplier},105,112,101,108,140\n")
            data = intraday.parse_klines_zip(payload)
            self.assertEqual(len(data), 2)
            self.assertEqual(data.timestamp.iloc[0], pd.Timestamp("2021-10-10", tz="UTC"))
            self.assertEqual(float(data.close.iloc[1]), 108)

    def test_malformed_zip_rejected(self):
        with self.assertRaises(ValueError):
            intraday.parse_klines_zip(zip_csv("open_time,open\n123,5\n"))
        with self.assertRaises(ValueError):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as z:
                z.writestr("not-a-csv.txt", "ignored")
            intraday.parse_klines_zip(buffer.getvalue())

    def test_strict_five_year_return_trade_and_coverage_gate(self):
        coverage = {"missing_or_irregular_intervals": 0}
        good = {"五年交易數": 70, "五年收益_pct": 100.01}
        self.assertTrue(intraday.qualifies(good, coverage))
        self.assertFalse(intraday.qualifies({**good, "五年收益_pct": 100.0}, coverage))
        self.assertFalse(intraday.qualifies({**good, "五年交易數": 69}, coverage))
        self.assertFalse(intraday.qualifies(good, {"missing_or_irregular_intervals": 1}))

    def test_partial_rankings_preserved_as_separate_intraday_files(self):
        coverage = {
            "symbol": "BTCUSDT", "timeframe": "1h",
            "missing_or_irregular_intervals": 0,
        }
        rows = [
            {"策略": "EMA20_50_ADX20", "五年交易數": 70, "五年收益_pct": 101.0},
            {"策略": "Turtle55_20_EMA200", "五年交易數": 100, "五年收益_pct": 99.0},
        ]
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(intraday, "OUTPUT", Path(folder)):
                intraday.write_rankings(rows, coverage)
                prefix = Path(folder) / "new_BTCUSDT_1h_five_year"
                ranking = pd.read_csv(str(prefix) + "_ranking.csv")
                self.assertEqual(ranking["策略"].tolist(), ["EMA20_50_ADX20", "Turtle55_20_EMA200"])
                self.assertEqual(ranking["符合門檻"].tolist(), [True, False])
                metadata = json.loads(Path(str(prefix) + "_provenance.json").read_text())
                self.assertEqual(metadata["qualified_rows"], 1)


    def test_capital_stop_excludes_unexecuted_signal_exit_counts(self):
        trades = [
            {"entry_time": "2022-01-01T00:00:00Z", "R": -10.0, "reason": "止損"},
            {"entry_time": "2025-11-01T00:00:00Z", "R": 3.0, "reason": "止盈"},
        ]
        full, executed, is_exec, oos_exec, reasons, oos_pct = intraday.summarize_execution(trades, 0.10)
        self.assertEqual(full[2], 1)
        self.assertTrue(full[3])
        self.assertEqual(len(executed), 1)
        self.assertEqual(len(is_exec), 1)
        self.assertEqual(len(oos_exec), 0)
        self.assertEqual(reasons.get("止損", 0), 1)
        self.assertEqual(reasons.get("止盈", 0), 0)
        self.assertEqual(oos_pct, 0.0)

    def test_oos_return_uses_executed_stake_without_account_reset(self):
        trades = [
            {"entry_time": "2022-01-01T00:00:00Z", "R": 1.0, "reason": "止盈"},
            {"entry_time": "2025-11-01T00:00:00Z", "R": -0.5, "reason": "止損"},
        ]
        full, executed, is_exec, oos_exec, reasons, oos_pct = intraday.summarize_execution(trades, 0.10)
        self.assertEqual(full[2], 2)
        self.assertEqual(len(oos_exec), 1)
        self.assertAlmostEqual(oos_pct, -5.0)

    def test_zero_trade_kelly_variant_never_occupies_top50(self):
        coverage = {"symbol": "BTCUSDT", "timeframe": "1h",
                    "missing_or_irregular_intervals": 0}
        rows = [
            {"策略": "NoRisk", "五年交易數": 0, "五年收益_pct": 0.0},
            {"策略": "Executed", "五年交易數": 100, "五年收益_pct": -90.0},
        ]
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(intraday, "OUTPUT", Path(folder)):
                intraday.write_rankings(rows, coverage)
                prefix = Path(folder) / "new_BTCUSDT_1h_five_year"
                all_rows = pd.read_csv(str(prefix) + "_ranking.csv")
                top50 = pd.read_csv(str(prefix) + "_top50.csv")
                self.assertEqual(all_rows["策略"].tolist(), ["Executed", "NoRisk"])
                self.assertEqual(top50["策略"].tolist(), ["Executed"])
                self.assertEqual(all_rows["有實際成交"].tolist(), [True, False])
                metadata = json.loads(Path(str(prefix) + "_provenance.json").read_text())
                self.assertEqual(metadata["zero_execution_rows"], 1)
                self.assertEqual(metadata["executed_ranking_rows"], 1)


if __name__ == "__main__":
    unittest.main()
