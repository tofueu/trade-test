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
import tempfile
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
INTERVALS = {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120, "4h": 240, "6h": 360, "8h": 480, "12h": 720, "1d": 1440}
# Longer single-timeframe bars need enough historical candles for EMA200.
# Keep the existing 2021-09 warm-up where it already supplies >=250 bars.
MIN_WARMUP_BARS = 250
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
    # Binance archives use either millisecond or microsecond integer epochs.
    # Never infer the unit from the maximum alone: a mixed-unit archive would
    # silently move its millisecond rows to 1970 when interpreted as "us".
    if not np.isfinite(timestamps.to_numpy(dtype=float)).all():
        raise ValueError("Non-finite Binance candle timestamp")
    if not (timestamps % 1 == 0).all():
        raise ValueError("Fractional Binance candle timestamp")
    microseconds = timestamps >= 10**14
    if microseconds.any() and not microseconds.all():
        raise ValueError("Mixed Binance timestamp units in archive")
    unit = "us" if microseconds.all() else "ms"
    raw["timestamp"] = pd.to_datetime(timestamps, unit=unit, utc=True)
    for column in ("open", "high", "low", "close", "volume"):
        raw[column] = pd.to_numeric(raw[column], errors="raise")
    validate_ohlcv(raw)
    return raw[["timestamp", "open", "high", "low", "close", "volume"]]


def validate_ohlcv(frame: pd.DataFrame) -> None:
    """Fail closed on malformed exchange candles, including poisoned local cache."""
    values = frame[["open", "high", "low", "close", "volume"]]
    if not np.isfinite(values.to_numpy(dtype=float)).all():
        raise ValueError("Non-finite Binance OHLCV value")
    if (frame[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("Non-positive Binance OHLC price")
    if (frame["volume"] < 0).any():
        raise ValueError("Negative Binance volume")
    if ((frame["high"] < frame[["open", "low", "close"]].max(axis=1)) |
            (frame["low"] > frame[["open", "high", "close"]].min(axis=1))).any():
        raise ValueError("Inconsistent Binance OHLC range")
    if frame["timestamp"].isna().any():
        raise ValueError("Missing Binance candle timestamp")


def deduplicate_verified_candles(candles: pd.DataFrame) -> pd.DataFrame:
    """Accept identical archive overlap but reject conflicting market candles.

    Monthly/daily ZIP overlap can repeat a timestamp. Silently keeping the
    first row when OHLCV differs would make five-year results depend on the
    order of downloaded archives, so treat conflicts as invalid source data.
    """
    duplicates = candles[candles.duplicated("timestamp", keep=False)]
    if not duplicates.empty:
        fields = ["open", "high", "low", "close", "volume"]
        distinct = duplicates.groupby("timestamp", sort=False)[fields].nunique(dropna=False)
        if distinct.gt(1).any().any():
            raise ValueError("Conflicting Binance OHLCV at duplicate timestamp")
    return candles.drop_duplicates("timestamp")


def download_archive(url: str) -> pd.DataFrame:
    request = urllib.request.Request(url, headers={"User-Agent": "TradeTest-RealIntraday/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return parse_klines_zip(response.read())



def restore_gap_klines_from_binance_daily_archive(
        candles: pd.DataFrame, symbol: str, interval: str,
        step: pd.Timedelta) -> tuple[pd.DataFrame, list[dict]]:
    """Repair *archive omissions* only with independently downloadable Binance
    historical daily ZIP candle rows (never forward-fill or interpolation).

    Each expected missing timestamp must be supplied as a real, structurally
    validated kline by the same venue/symbol/interval. Fail closed otherwise.
    """
    ordered = candles.sort_values("timestamp").reset_index(drop=True)
    tested = ordered[(ordered.timestamp >= START) & (ordered.timestamp < END)]
    delta = tested.timestamp.diff()
    missing = []
    for idx in delta[delta > step].index:
        current = tested.loc[idx, "timestamp"]
        previous = tested.loc[idx-1, "timestamp"]
        if (current - previous) % step != pd.Timedelta(0):
            raise RuntimeError("Non-aligned exchange candle gap cannot be repaired")
        n = int((current-previous)//step) - 1
        if n <= 0:
            continue
        if n > 18000 or len(missing) + n > 24000:
            raise RuntimeError("Exchange archive gap exceeds safe repair audit limit")
        missing.extend(pd.date_range(previous+step, periods=n, freq=step))
    if not missing:
        return ordered, []
    wanted = set(missing)
    days = sorted({t.strftime("%Y-%m-%d") for t in missing})
    if len(days) > 20:
        raise RuntimeError("Too many missing days for explicit daily archive audit")
    print("BINANCE_ARCHIVE_GAP_DAYS", symbol, interval, days, flush=True)
    restored, receipts = [], []
    for day in days:
        filename = f"{symbol}-{interval}-{day}.zip"
        url = f"{SOURCE}/daily/klines/{symbol}/{interval}/{filename}"
        request = urllib.request.Request(
            url, headers={"User-Agent": "TradeTest-Audit-GapRepair/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        daily = parse_klines_zip(payload)
        daily = daily[daily.timestamp.isin(wanted)].copy()
        if daily.empty:
            raise RuntimeError(f"Binance daily archive lacks missing rows: {url}")
        if daily.timestamp.duplicated().any():
            raise RuntimeError(f"Conflicting duplicate Binance daily timestamps: {url}")
        receipts.append({
            "archive_url": url, "zip_sha256": hashlib.sha256(payload).hexdigest(),
            "restored_bar_count": int(len(daily))})
        restored.append(daily)
        print("VERIFIED_EXCHANGE_DAILY_ARCHIVE", day, len(daily), flush=True)
    candidate = pd.concat([ordered, *restored], ignore_index=True)
    candidate = deduplicate_verified_candles(candidate)
    candidate = candidate.sort_values("timestamp").reset_index(drop=True)
    restored_times = set(pd.concat(restored).timestamp)
    if restored_times != wanted:
        raise RuntimeError(
            f"Binance daily audit incomplete: wanted={len(wanted)}, "
            f"verified={len(restored_times)}, missing={len(wanted-restored_times)}")
    validate_ohlcv(candidate)
    print("REAL_EXCHANGE_GAP_REPAIR_COMPLETE", symbol, interval,
          "restored_bars", len(wanted), flush=True)
    return candidate, receipts


def load_real_ohlcv(symbol: str, interval: str) -> tuple[pd.DataFrame, dict]:
    if symbol not in ("BTCUSDT", "ETHUSDT", "SOLUSDT") or interval not in INTERVALS:
        raise ValueError("Only confirmed Binance USD-M futures symbols and kline intervals are supported")
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE / f"{symbol}_{interval}_{START:%Y%m%d}_{END:%Y%m%d}.csv"
    step = pd.Timedelta(minutes=INTERVALS[interval])
    warm_start = min(WARM, START - MIN_WARMUP_BARS * step)
    cache_hit = cache_file.exists()
    if cache_hit:
        candles = pd.read_csv(cache_file, parse_dates=["timestamp"])
        candles["timestamp"] = pd.to_datetime(candles["timestamp"], utc=True)
    else:
        frames = []
        for month in pd.period_range(warm_start.strftime("%Y-%m"), ARCHIVE_LAST_MONTH, freq="M"):
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
        candles = deduplicate_verified_candles(candles).sort_values("timestamp")
        candles = candles[(candles.timestamp >= warm_start) & (candles.timestamp < END)]
    candles = candles.sort_values("timestamp").reset_index(drop=True)
    # Cached CSVs are not trusted: validate again before accepting coverage.
    validate_ohlcv(candles)
    in_window = candles[(candles.timestamp >= START) & (candles.timestamp < END)]
    if in_window.empty or in_window.timestamp.iloc[0] > START or in_window.timestamp.iloc[-1] < END - step:
        raise RuntimeError("Five-year historical coverage incomplete; no qualified ranking")
    # Indicator signals depend on pre-window candles (EMA200, ATR, ADX).
    # A truncated cache can otherwise pass the five-year in-window test while
    # silently changing strategy entries and the reported performance.
    warmup = candles[(candles.timestamp >= warm_start) & (candles.timestamp < START)]
    if (warmup.empty or warmup.timestamp.iloc[0] != warm_start
            or warmup.timestamp.iloc[-1] != START - step
            or (warmup.timestamp.diff().dropna() != step).any()):
        raise RuntimeError("Indicator warm-up history incomplete; no qualified ranking")
    diffs = in_window.timestamp.diff().dropna()
    gaps = int((diffs != step).sum())
    gap_repair_receipts = []
    if gaps and not cache_hit:
        candles, gap_repair_receipts = restore_gap_klines_from_binance_daily_archive(
            candles, symbol, interval, step)
        in_window = candles[(candles.timestamp >= START) & (candles.timestamp < END)]
        diffs = in_window.timestamp.diff().dropna()
        gaps = int((diffs != step).sum())
    if gaps:
        bad = in_window.loc[diffs[diffs != step].index, "timestamp"].head(16)
        prior = in_window["timestamp"].shift(1).loc[bad.index]
        details = [{"previous": p.isoformat(), "next": n.isoformat(),
                    "delta": str(n-p)} for p, n in zip(prior, bad)]
        raise RuntimeError(
            f"Irregular or missing five-year candles; {symbol}/{interval} "
            f"gaps={gaps} first_gaps={json.dumps(details)}; "
            "do not qualify or fill nonexistent bars")
    # Never poison the cache with a partial download. Commit only fully
    # validated history, atomically, so a later run can retry from the source.
    if not cache_hit:
        temporary = cache_file.with_name(cache_file.name + f".{os.getpid()}.tmp")
        try:
            candles.to_csv(temporary, index=False)
            os.replace(temporary, cache_file)
        finally:
            if temporary.exists():
                temporary.unlink()
    digest = hashlib.sha256(
        pd.util.hash_pandas_object(candles, index=False).values.tobytes()).hexdigest()
    coverage = {
        "source": SOURCE, "symbol": symbol, "timeframe": interval,
        "warmup_start_utc": warm_start.isoformat(),
        "warmup_bar_count": int(len(warmup)),
        "min_warmup_bars": MIN_WARMUP_BARS,
        "start_utc": START.isoformat(), "end_exclusive_utc": END.isoformat(),
        "actual_first_utc": in_window.timestamp.iloc[0].isoformat(),
        "actual_last_utc": in_window.timestamp.iloc[-1].isoformat(),
        "bar_count": int(len(in_window)), "missing_or_irregular_intervals": gaps,
        "ohlcv_sha256": digest, "historical_data": True,
        "verified_daily_archive_gap_repair": gap_repair_receipts,
        "daily_archives_added": len(gap_repair_receipts),
        "tradingview_run_verified": False, "pine_v6_parity_verified": False,
        "cost_model": "existing Binance USD-M 5bps/side slippage + 5bps/side taker fee",
    }
    return candles, coverage


def qualifies(row: dict, coverage: dict) -> bool:
    return (coverage["missing_or_irregular_intervals"] == 0
            and int(row["五年交易數"]) >= 70
            and float(row["五年收益_pct"]) > 100.0)


def summarize_execution(trades: list[dict], fraction: float):
    """Restrict trade and exit statistics to positions actually funded/executed.

    The shared legacy fixed-risk engine halts when available equity is too low;
    trades after that point are hypothetical signals, not executed fills.
    """
    full = base.fixed_risk_stats(trades, fraction)
    # The legacy daily engine records peak-to-trough drawdown before flooring
    # a bankrupt account at zero. A final gap loss can therefore report >100%
    # drawdown even though this cash-equity model does not permit debt. Keep
    # its actual return, fill count and halt decision, but cap drawdown at the
    # 100% loss of all starting equity. Do not rewrite legacy daily results.
    full = (full[0], min(100.0, max(0.0, full[1])), full[2], full[3])
    executed = trades[:int(full[2])]
    is_executed = [t for t in executed if pd.Timestamp(t["entry_time"]) < OOS]
    oos_executed = [t for t in executed if pd.Timestamp(t["entry_time"]) >= OOS]
    reasons = pd.Series([t["reason"] for t in executed]).value_counts().to_dict() if executed else {}
    # OOS P&L is expressed against the original capital, without restarting a
    # bankrupt/underfunded strategy with a fresh account at the OOS boundary.
    oos_return_pct = 100.0 * fraction * sum(float(t["R"]) for t in oos_executed)
    return full, executed, is_executed, oos_executed, reasons, oos_return_pct


def _atomic_write(path: Path, writer, encoding: str = "utf-8") -> None:
    """Preserve the previous ranking if serialization or replacement fails."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding=encoding, newline="", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            writer(handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def verify_ranking_snapshot(stem: str) -> dict:
    """Reject a torn multi-file checkpoint rather than trusting stale CSVs."""
    prefix = OUTPUT / stem
    manifest = json.loads(Path(str(prefix) + "_provenance.json").read_text(encoding="utf-8"))
    for suffix, field in (("_ranking.csv", "ranking_csv_sha256"),
                          ("_top50.csv", "top50_csv_sha256")):
        expected = manifest.get(field)
        if not isinstance(expected, str) or len(expected) != 64:
            raise ValueError(f"Missing verified ranking digest: {field}")
        actual = hashlib.sha256(Path(str(prefix) + suffix).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Ranking checkpoint digest mismatch: {field}")
    return manifest


def write_rankings(rows: list[dict], coverage: dict) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stem = f"new_{coverage['symbol']}_{coverage['timeframe']}_five_year"
    frame = pd.DataFrame(rows)
    frame["符合門檻"] = [qualifies(row, coverage) for row in frame.to_dict("records")]
    frame["有實際成交"] = frame["五年交易數"].astype(int) > 0
    # Do not let zero-risk Kelly variants (0 executed trades, 0% return)
    # outrank genuinely executed strategies that lost money.
    frame = frame.sort_values(["符合門檻", "有實際成交", "五年收益_pct"],
                              ascending=[False, False, False]).reset_index(drop=True)
    frame.insert(0, "新策略排名", np.arange(1, len(frame) + 1))
    ranking_path = OUTPUT / f"{stem}_ranking.csv"
    top50_path = OUTPUT / f"{stem}_top50.csv"
    provenance_path = OUTPUT / f"{stem}_provenance.json"
    # The runner can be interrupted between strategies. Replace each file
    # atomically; never truncate a previous good leaderboard in place.
    _atomic_write(ranking_path, lambda handle: frame.to_csv(handle, index=False),
                  encoding="utf-8-sig")
    executed_frame = frame[frame["有實際成交"]].head(50)
    _atomic_write(top50_path, lambda handle: executed_frame.to_csv(handle, index=False),
                  encoding="utf-8-sig")
    # JSON is the last commit marker. Its digests make a crash between the two
    # CSV replacements detectable instead of silently mixing generations.
    provenance = {
        **coverage, "completed_strategy_names": sorted(set(frame["策略"])),
        "ranking_rows": len(frame), "qualified_rows": int(frame["符合門檻"].sum()),
        "executed_ranking_rows": int(frame["有實際成交"].sum()),
        "zero_execution_rows": int((~frame["有實際成交"]).sum()),
        "ranking_csv_sha256": hashlib.sha256(ranking_path.read_bytes()).hexdigest(),
        "top50_csv_sha256": hashlib.sha256(top50_path.read_bytes()).hexdigest(),
        "oos_return_definition": "Executed OOS R times initial stake, divided by initial capital; no capital reset",
    }
    _atomic_write(provenance_path, lambda handle: json.dump(
        provenance, handle, ensure_ascii=False, indent=2))
    verify_ranking_snapshot(stem)
    print("RANKING", len(frame), "EXECUTED", int(frame["有實際成交"].sum()),
          "QUALIFIED", int(frame["符合門檻"].sum()), flush=True)

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
        for alloc, fraction in (("固定1R", .10), ("全凱利", kelly),
                                ("半凱利", kelly / 2), ("四分之一凱利", kelly / 4)):
            full, executed, is_executed, oos_executed, reasons, oos_return = summarize_execution(trades, fraction)
            wins = [float(t["R"]) for t in executed if float(t["R"]) > 0]
            losses = [-float(t["R"]) for t in executed if float(t["R"]) <= 0]
            rr = ((sum(wins) / len(wins)) / (sum(losses) / len(losses))) if wins and losses and sum(losses) > 0 else None
            rows.append({
                "市場": "Crypto futures", "商品": args.symbol, "代碼": args.symbol,
                "時區": args.timeframe, "策略": name, "策略規則": old.RULES[name],
                "出場方式": f"IS選定固定TP {tp:g}R／初始SL 1.5ATR＋策略出場",
                "倉位法": alloc, "五年交易數": int(full[2]),
                "策略訊號交易數": len(trades), "資金停止": bool(full[3]),
                "止盈出場數": int(reasons.get("止盈", 0)),
                "止損出場數": int(reasons.get("止損", 0)),
                "五年收益_pct": full[0], "五年最大回撤_pct": full[1],
                "五年勝率_pct": (100.0 * len(wins) / len(executed)) if executed else None,
                "五年盈虧比": rr,
                "五年獲利因子": (sum(wins) / sum(losses)) if losses and sum(losses) > 0 else None,
                "OOS收益_pct": oos_return, "OOS交易數": len(oos_executed),
                "IS交易數": len(is_executed), "IS_Kelly_pct": kelly * 100,
                "資料完整": coverage["missing_or_irregular_intervals"] == 0,
            })
        # Save a genuine, partial ranking after each completed strategy.
        write_rankings(rows, coverage)
        print("DONE_STRATEGY", name, "rows", len(rows), flush=True)


if __name__ == "__main__":
    main()
