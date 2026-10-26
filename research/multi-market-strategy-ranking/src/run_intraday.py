"""Real Binance USD-M intraday extension of the existing five-year Python engine.

No daily-to-intraday extrapolation, no synthetic candles, no TradingView claim.
A first BTCUSDT 1h batch uses the original signals, TP selection and risk stats.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import five_year_multi_market_kelly as base
import run_strategies as old

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "intraday"
CACHE = ROOT / "src" / "five_year_market_data" / "intraday"
INTERVALS = {"1h": 60, "30m": 30, "15m": 15, "5m": 5}
START = base.START
END = base.END
OOS = base.OOS
WARM = pd.Timestamp("2021-09-01", tz="UTC")
ARCHIVE_LAST_MONTH = "2026-09"
SOURCE = "https://data.binance.vision/data/futures/um"


def parse_klines_zip(payload: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = [name for name in archive.namelist() if name.endswith(".csv")]
        if len(members) != 1:
            raise ValueError("Expected exactly one Binance kline CSV in ZIP")
        raw = pd.read_csv(archive.open(members[0]), header=None)
    if len(raw) and str(raw.iloc[0, 0]).strip().lower() == "open_time":
        raw = raw.iloc[1:]
    if raw.empty or raw.shape[1] < 6:
        raise ValueError("Empty or incomplete Binance kline archive")
    raw = raw.iloc[:, :6].copy()
    raw.columns = ["open_time", "open", "high", "low", "close", "volume"]
    timestamps = pd.to_numeric(raw["open_time"], errors="raise")
    # Some Binance historical archives switched timestamp precision.
    unit = "us" if timestamps.max() >= 10**14 else "ms"
    raw["timestamp"] = pd.to_datetime(timestamps, unit=unit, utc=True)
    for column in ("open", "high", "low", "close", "volume"):
        raw[column] = pd.to_numeric(raw[column], errors="raise")
    if not np.isfinite(raw[["open", "high", "low", "close", "volume"]].to_numpy()).all():
        raise ValueError("Non-finite Binance OHLCV value")
    return raw[["timestamp", "open", "high", "low", "close", "volume"]]


def download_archive(url: str) -> pd.DataFrame:
    request = urllib.request.Request(url, headers={"User-Agent": "TradeTest-RealIntraday/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return parse_klines_zip(response.read())


def load_real_ohlcv(symbol: str, interval: str) -> tuple[pd.DataFrame, dict]:
    if symbol != "BTCUSDT" or interval not in INTERVALS:
        raise ValueError("First verified batch supports BTCUSDT and known intraday intervals only")
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE / f"{symbol}_{interval}_{START:%Y%m%d}_{END:%Y%m%d}.csv"
    if cache_file.exists():
        candles = pd.read_csv(cache_file, parse_dates=["timestamp"])
        candles["timestamp"] = pd.to_datetime(candles["timestamp"], utc=True)
    else:
        frames = []
        for month in pd.period_range("2021-09", ARCHIVE_LAST_MONTH, freq="M"):
            name = f"{symbol}-{interval}-{month}.zip"
            url = f"{SOURCE}/monthly/klines/{symbol}/{interval}/{name}"
            frames.append(download_archive(url))
            print("FETCHED", name, flush=True)
        for day in pd.date_range("2026-10-01", "2026-10-09", freq="D"):
            ds = day.strftime("%Y-%m-%d")
            name = f"{symbol}-{interval}-{ds}.zip"
            url = f"{SOURCE}/daily/klines/{symbol}/{interval}/{name}"
            frames.append(download_archive(url))
            print("FETCHED", name, flush=True)
        candles = pd.concat(frames, ignore_index=True)
        candles = candles.drop_duplicates("timestamp").sort_values("timestamp")
        candles = candles[(candles.timestamp >= WARM) & (candles.timestamp < END)]
        candles.to_csv(cache_file, index=False)
    candles = candles.sort_values("timestamp").reset_index(drop=True)
    step = pd.Timedelta(minutes=INTERVALS[interval])
    in_window = candles[(candles.timestamp >= START) & (candles.timestamp < END)]
    if in_window.empty or in_window.timestamp.iloc[0] > START or in_window.timestamp.iloc[-1] < END - step:
        raise RuntimeError("Five-year historical coverage incomplete; no qualified ranking")
    diffs = in_window.timestamp.diff().dropna()
    gaps = int((diffs != step).sum())
    digest = hashlib.sha256(
        pd.util.hash_pandas_object(candles, index=False).values.tobytes()).hexdigest()
    coverage = {
        "source": SOURCE, "symbol": symbol, "timeframe": interval,
        "start_utc": START.isoformat(), "end_exclusive_utc": END.isoformat(),
        "actual_first_utc": in_window.timestamp.iloc[0].isoformat(),
        "actual_last_utc": in_window.timestamp.iloc[-1].isoformat(),
        "bar_count": int(len(in_window)), "missing_or_irregular_intervals": gaps,
        "ohlcv_sha256": digest, "historical_data": True,
        "tradingview_run_verified": False, "pine_v6_parity_verified": False,
        "cost_model": "existing Binance USD-M 5bps/side slippage + 5bps/side taker fee",
    }
    return candles, coverage


def qualifies(row: dict, coverage: dict) -> bool:
    return (coverage["missing_or_irregular_intervals"] == 0
            and int(row["五年交易數"]) >= 70
            and float(row["五年收益_pct"]) > 100.0)


def write_rankings(rows: list[dict], coverage: dict) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stem = f"new_{coverage['symbol']}_{coverage['timeframe']}_five_year"
    frame = pd.DataFrame(rows).sort_values("五年收益_pct", ascending=False)
    frame = frame.reset_index(drop=True)
    frame.insert(0, "新策略排名", np.arange(1, len(frame) + 1))
    frame["符合門檻"] = [qualifies(row, coverage) for row in frame.to_dict("records")]
    frame.to_csv(OUTPUT / f"{stem}_ranking.csv", index=False, encoding="utf-8-sig")
    frame.head(50).to_csv(OUTPUT / f"{stem}_top50.csv", index=False, encoding="utf-8-sig")
    with (OUTPUT / f"{stem}_provenance.json").open("w", encoding="utf-8") as f:
        json.dump({**coverage, "completed_strategy_names": sorted(set(frame["策略"])),
                   "ranking_rows": len(frame), "qualified_rows": int(frame["符合門檻"].sum())},
                  f, ensure_ascii=False, indent=2)
    print("RANKING", len(frame), "QUALIFIED", int(frame["符合門檻"].sum()), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT", choices=["BTCUSDT"])
    parser.add_argument("--timeframe", default="1h", choices=list(INTERVALS))
    args = parser.parse_args()
    raw, coverage = load_real_ohlcv(args.symbol, args.timeframe)
    print("REAL_DATA", json.dumps(coverage, ensure_ascii=False), flush=True)
    rows = []
    for name in old.RULES:
        variants = []
        for tp in old.TP_RS:
            trades = old.run(raw, "Crypto futures", args.symbol, name, tp)
            is_tr = [t for t in trades if pd.Timestamp(t["entry_time"]) < OOS
                     and pd.Timestamp(t["exit_time"]) < OOS]
            ret, dd, _, _ = base.fixed_risk_stats(is_tr, .10)
            variants.append((tp, trades, is_tr, ret, dd))
        eligible = [v for v in variants if len(v[2]) >= 20 and v[3] > 0]
        if not eligible:
            eligible = [v for v in variants if v[3] > 0] or variants
        tp, trades, is_tr, _, _ = max(
            eligible, key=lambda v: (v[3] / max(v[4], 1.), v[3], len(v[2])))
        oos_tr = [t for t in trades if pd.Timestamp(t["entry_time"]) >= OOS]
        kelly = base.formula_stats(is_tr)["kelly"]
        kelly = max(0., float(kelly)) if math.isfinite(kelly) else 0.
        reasons = pd.Series([t["reason"] for t in trades]).value_counts().to_dict()
        for alloc, fraction in (("固定1R", .10), ("全凱利", kelly),
                                ("半凱利", kelly / 2), ("四分之一凱利", kelly / 4)):
            full = base.fixed_risk_stats(trades, fraction)
            oos = base.fixed_risk_stats(oos_tr, fraction)
            rows.append({
                "市場": "Crypto futures", "商品": args.symbol, "代碼": args.symbol,
                "時區": args.timeframe, "策略": name, "策略規則": old.RULES[name],
                "出場方式": f"IS選定固定TP {tp:g}R／初始SL 1.5ATR＋策略出場",
                "倉位法": alloc, "五年交易數": len(trades),
                "止盈出場數": int(reasons.get("止盈", 0)),
                "止損出場數": int(reasons.get("止損", 0)),
                "五年收益_pct": full[0], "五年最大回撤_pct": full[1],
                "OOS收益_pct": oos[0], "OOS交易數": len(oos_tr),
                "IS交易數": len(is_tr), "IS_Kelly_pct": kelly * 100,
                "資料完整": coverage["missing_or_irregular_intervals"] == 0,
            })
        # Save a genuine, partial ranking after each completed strategy.
        write_rankings(rows, coverage)
        print("DONE_STRATEGY", name, "rows", len(rows), flush=True)


if __name__ == "__main__":
    main()
