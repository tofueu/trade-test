"""Offline tests for real intraday loader and strict qualification (no network)."""
import hashlib
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

    def test_mixed_and_fractional_binance_timestamps_rejected(self):
        ms = 1633824000000
        us = 1633827600000000
        mixed = (f"{ms},100,110,90,105,1\n"
                 f"{us},105,112,101,108,2\n")
        with self.assertRaisesRegex(ValueError, "Mixed Binance timestamp units"):
            intraday.parse_klines_zip(zip_csv(mixed))
        fractional = f"{ms}.5,100,110,90,105,1\n"
        with self.assertRaisesRegex(ValueError, "Fractional Binance candle timestamp"):
            intraday.parse_klines_zip(zip_csv(fractional))
        nonfinite = "NaN,100,110,90,105,1\n"
        with self.assertRaisesRegex(ValueError, "Non-finite Binance candle timestamp"):
            intraday.parse_klines_zip(zip_csv(nonfinite))

    def test_malformed_zip_rejected(self):
        with self.assertRaises(ValueError):
            intraday.parse_klines_zip(zip_csv("open_time,open\n123,5\n"))
        with self.assertRaises(ValueError):
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as z:
                z.writestr("not-a-csv.txt", "ignored")
            intraday.parse_klines_zip(buffer.getvalue())

    def test_archive_overlap_must_not_silently_choose_conflicting_ohlcv(self):
        timestamp = pd.Timestamp("2021-10-10T00:00:00Z")
        first = {"timestamp": timestamp, "open": 100, "high": 110,
                 "low": 90, "close": 105, "volume": 1}
        identical = pd.DataFrame([first, first.copy()])
        conflicting = pd.DataFrame([first, {**first, "close": 106}])
        self.assertEqual(len(intraday.deduplicate_verified_candles(identical)), 1)
        with self.assertRaisesRegex(ValueError, "Conflicting Binance OHLCV"):
            intraday.deduplicate_verified_candles(conflicting)

        # Exercise the real archive-aggregation path, not only the helper.
        # A conflict must fail before any partially validated CSV is cached.
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            with (patch.object(intraday, "CACHE", cache),
                  patch.object(intraday, "START", timestamp),
                  patch.object(intraday, "END", timestamp + pd.Timedelta(hours=2)),
                  patch.object(intraday, "WARM", timestamp - pd.Timedelta(hours=2)),
                  patch.object(intraday, "MIN_WARMUP_BARS", 1),
                  patch.object(intraday, "download_archive", return_value=conflicting)):
                with self.assertRaisesRegex(ValueError, "Conflicting Binance OHLCV"):
                    intraday.load_real_ohlcv("BTCUSDT", "1h")
                self.assertFalse(any(cache.iterdir()))

    def test_invalid_exchange_ohlcv_rejected_before_ranking(self):
        invalid_rows = (
            "1633824000000,100,99,90,105,1\n",
            "1633824000000,100,110,90,105,-1\n",
            "1633824000000,0,110,90,105,1\n",
        )
        for row in invalid_rows:
            with self.subTest(row=row), self.assertRaises(ValueError):
                intraday.parse_klines_zip(zip_csv(row))

    def test_cached_ohlcv_is_validated_before_coverage_claim(self):
        start = pd.Timestamp("2021-10-10T00:00:00Z")
        end = pd.Timestamp("2021-10-10T02:00:00Z")
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            name = cache / "BTCUSDT_1h_20211010_20211010.csv"
            pd.DataFrame({
                "timestamp": [start, start + pd.Timedelta(hours=1)],
                "open": [100, 100], "high": [99, 110],
                "low": [90, 90], "close": [105, 105], "volume": [1, 1],
            }).to_csv(name, index=False)
            with (patch.object(intraday, "CACHE", cache),
                  patch.object(intraday, "START", start),
                  patch.object(intraday, "END", end)):
                with self.assertRaisesRegex(ValueError, "OHLC range"):
                    intraday.load_real_ohlcv("BTCUSDT", "1h")

    def test_missing_indicator_warmup_cannot_pass_five_year_coverage(self):
        start = pd.Timestamp("2021-10-10T00:00:00Z")
        end = start + pd.Timedelta(hours=2)
        warm = start - pd.Timedelta(days=1)
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            path = cache / "BTCUSDT_1h_20211010_20211010.csv"
            times = pd.date_range(warm + pd.Timedelta(hours=1),
                                  end - pd.Timedelta(hours=1), freq="h")
            pd.DataFrame({
                "timestamp": times, "open": 100, "high": 110,
                "low": 90, "close": 105, "volume": 1,
            }).to_csv(path, index=False)
            with (patch.object(intraday, "CACHE", cache),
                  patch.object(intraday, "WARM", warm),
                  patch.object(intraday, "MIN_WARMUP_BARS", 1),
                  patch.object(intraday, "START", start),
                  patch.object(intraday, "END", end)):
                with self.assertRaisesRegex(RuntimeError, "warm-up"):
                    intraday.load_real_ohlcv("BTCUSDT", "1h")
                # Complete warm-up history must still be accepted.
                times = pd.date_range(warm, end - pd.Timedelta(hours=1), freq="h")
                pd.DataFrame({
                    "timestamp": times, "open": 100, "high": 110,
                    "low": 90, "close": 105, "volume": 1,
                }).to_csv(path, index=False)
                _, provenance = intraday.load_real_ohlcv("BTCUSDT", "1h")
                self.assertEqual(provenance["missing_or_irregular_intervals"], 0)
                self.assertEqual(provenance["bar_count"], 2)

    def test_all_requested_independent_timeframes_are_supported(self):
        expected = {
            "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30,
            "1h": 60, "2h": 120, "4h": 240, "6h": 360,
            "8h": 480, "12h": 720, "1d": 1440,
        }
        self.assertEqual(intraday.INTERVALS, expected)

    def test_daily_ema200_warmup_uses_real_prior_candles(self):
        start = pd.Timestamp("2021-10-10T00:00:00Z")
        end = start + pd.Timedelta(days=2)
        warm = start - pd.Timedelta(days=250)
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            path = cache / "BTCUSDT_1d_20211010_20211012.csv"
            times = pd.date_range(warm, end - pd.Timedelta(days=1), freq="D")
            pd.DataFrame({
                "timestamp": times, "open": 100, "high": 110,
                "low": 90, "close": 105, "volume": 1,
            }).to_csv(path, index=False)
            with (patch.object(intraday, "CACHE", cache),
                  patch.object(intraday, "WARM", start - pd.Timedelta(days=39)),
                  patch.object(intraday, "START", start),
                  patch.object(intraday, "END", end)):
                _, coverage = intraday.load_real_ohlcv("BTCUSDT", "1d")
                self.assertEqual(coverage["warmup_bar_count"], 250)
                self.assertEqual(coverage["warmup_start_utc"], warm.isoformat())
                self.assertEqual(coverage["bar_count"], 2)
                # Existing 39-day warm-up must never qualify daily EMA200.
                truncated = pd.read_csv(path)
                truncated = truncated.iloc[-41:]
                truncated.to_csv(path, index=False)
                with self.assertRaisesRegex(RuntimeError, "warm-up"):
                    intraday.load_real_ohlcv("BTCUSDT", "1d")

    def test_incomplete_download_never_poisoned_cache(self):
        start = pd.Timestamp("2021-10-10T00:00:00Z")
        end = start + pd.Timedelta(hours=2)
        warm = start - pd.Timedelta(days=1)
        # All mocked archives contain only one hour: cannot cover two hours.
        partial = pd.DataFrame({
            "timestamp": [start], "open": [100], "high": [110],
            "low": [90], "close": [105], "volume": [1],
        })
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            with (patch.object(intraday, "CACHE", cache),
                  patch.object(intraday, "WARM", warm),
                  patch.object(intraday, "START", start),
                  patch.object(intraday, "END", end),
                  patch.object(intraday, "download_archive", return_value=partial)):
                with self.assertRaisesRegex(RuntimeError, "coverage incomplete"):
                    intraday.load_real_ohlcv("BTCUSDT", "1h")
                self.assertFalse((cache / "BTCUSDT_1h_20211010_20211010.csv").exists())

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


    def test_intraday_rankings_are_atomic_and_provenance_hashes_match(self):
        coverage = {"symbol": "BTCUSDT", "timeframe": "1h",
                    "missing_or_irregular_intervals": 0}
        rows = [{"策略": "EMA20_50_ADX20", "五年交易數": 70,
                 "五年收益_pct": 110.0}]
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            with patch.object(intraday, "OUTPUT", output):
                intraday.write_rankings(rows, coverage)
                prefix = output / "new_BTCUSDT_1h_five_year"
                ranking = Path(str(prefix) + "_ranking.csv")
                top50 = Path(str(prefix) + "_top50.csv")
                provenance = Path(str(prefix) + "_provenance.json")
                baseline = {path: path.read_bytes() for path in
                            (ranking, top50, provenance)}
                manifest = json.loads(provenance.read_text(encoding="utf-8"))
                self.assertEqual(intraday.verify_ranking_snapshot(prefix.name), manifest)
                self.assertEqual(manifest["ranking_csv_sha256"],
                                 hashlib.sha256(ranking.read_bytes()).hexdigest())
                self.assertEqual(manifest["top50_csv_sha256"],
                                 hashlib.sha256(top50.read_bytes()).hexdigest())
                # A failed atomic replacement must not truncate a prior result.
                with patch.object(intraday.os, "replace",
                                  side_effect=OSError("simulated replace failure")):
                    with self.assertRaisesRegex(OSError, "simulated replace failure"):
                        intraday.write_rankings(
                            [{**rows[0], "五年收益_pct": -20.0}], coverage)
                for path, expected in baseline.items():
                    self.assertEqual(path.read_bytes(), expected)
                self.assertEqual(list(output.glob(".*.tmp")), [])

    def test_interrupted_multi_file_checkpoint_is_detectable_by_digest(self):
        coverage = {"symbol": "BTCUSDT", "timeframe": "1h",
                    "missing_or_irregular_intervals": 0}
        first = [{"策略": "EMA20_50_ADX20", "五年交易數": 70,
                  "五年收益_pct": 110.0}]
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            with patch.object(intraday, "OUTPUT", output):
                intraday.write_rankings(first, coverage)
                prefix = output / "new_BTCUSDT_1h_five_year"
                ranking = Path(str(prefix) + "_ranking.csv")
                provenance = Path(str(prefix) + "_provenance.json")
                old_digest = json.loads(provenance.read_text())["ranking_csv_sha256"]
                original_replace = intraday.os.replace
                replacements = 0

                def fail_on_second_replace(source, destination):
                    nonlocal replacements
                    replacements += 1
                    if replacements == 2:
                        raise OSError("second file replacement interrupted")
                    return original_replace(source, destination)

                with patch.object(intraday.os, "replace",
                                  side_effect=fail_on_second_replace):
                    with self.assertRaisesRegex(OSError, "second file"):
                        intraday.write_rankings(
                            [{**first[0], "五年收益_pct": -20.0}], coverage)
                self.assertNotEqual(old_digest,
                                    hashlib.sha256(ranking.read_bytes()).hexdigest())
                with self.assertRaisesRegex(ValueError, "digest mismatch"):
                    intraday.verify_ranking_snapshot(prefix.name)
                self.assertEqual(list(output.glob(".*.tmp")), [])

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

    def test_bankruptcy_drawdown_never_exceeds_100_percent(self):
        # Legacy fixed_risk_stats computes drawdown before it floors equity
        # at zero; an adverse gap with R=-11 at 10% risk produced 110% DD.
        trades = [{"entry_time": "2022-01-01T00:00:00Z",
                   "R": -11.0, "reason": "止損"}]
        legacy = intraday.base.fixed_risk_stats(trades, 0.10)
        self.assertGreater(legacy[1], 100.0)
        full, executed, _, _, reasons, _ = intraday.summarize_execution(trades, 0.10)
        self.assertEqual(full[0], -100.0)
        self.assertEqual(full[1], 100.0)
        self.assertEqual(full[2], 1)
        self.assertTrue(full[3])
        self.assertEqual(len(executed), 1)
        self.assertEqual(reasons["止損"], 1)

    def test_normal_drawdown_is_unchanged(self):
        trades = [{"entry_time": "2022-01-01T00:00:00Z",
                   "R": -1.0, "reason": "止損"}]
        legacy = intraday.base.fixed_risk_stats(trades, 0.10)
        full, *_ = intraday.summarize_execution(trades, 0.10)
        self.assertEqual(full, legacy)

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
