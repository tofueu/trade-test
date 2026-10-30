"""Real five-year intraday re-backtest of ALL old strategy families.

Run each (timeframe, family) separately. Preserve existing original test code:
  original: eight original signals, nine original exits;
  compound: eight two-signal/weekly-confirmation strategies, nine exits;
  fixed: nine indicator composites, five IS-selectable TP targets.
New seven strategies were already independently run over all 12 timeframes in
run_intraday.py and their provenance is checked by aggregate_all_timeframes.py.

No invented candles, no daily-to-intraday extrapolation; unavailable data
is reported as a failure, not as a zero-return strategy.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
import five_year_multi_market_kelly as base
import five_year_exit_method_sweep as exits
import run_intraday as intraday

OUT = ROOT / "results" / "all_timeframes"
FAMILIES = ("original", "compound", "fixed", "new")
DERIVED = {
    "2m": ("1m", 2), "10m": ("5m", 2),
    "20m": ("5m", 4), "45m": ("15m", 3), "3h": ("1h", 3),
}
PERIODS = tuple(intraday.INTERVALS) + tuple(DERIVED)
SYMBOL_MARKET = {
    "BTCUSDT": "Crypto futures", "ETHUSDT": "Crypto futures",
    "SOLUSDT": "Crypto futures",
    "GC=F": "Traditional futures", "SI=F": "Traditional futures",
    "ES=F": "Traditional futures", "NQ=F": "Traditional futures",
    "USDJPY=X": "FX", "^TWII": "Index benchmark (nontradable)",
}

def load_market_ohlcv(symbol, timeframe):
    market = SYMBOL_MARKET[symbol]
    if market == "Crypto futures":
        base_tf, ratio = DERIVED.get(timeframe, (timeframe, 1))
        frame, coverage = intraday.load_real_ohlcv(symbol, base_tf)
        if ratio > 1:
            # Each derived bar consists exclusively of the expected number of
            # consecutive, exchange-recorded OHLCV source bars, never of
            # invented interpolated K-lines. UTC origin matches crypto candles.
            mins = intraday.INTERVALS[base_tf] * ratio
            buckets = frame["timestamp"].dt.floor(f"{mins}min")
            group = frame.groupby(buckets, sort=True)
            counts = group.size()
            agg = group.agg({
                "open": "first", "high": "max", "low": "min",
                "close": "last", "volume": "sum"
            }).reset_index()
            target_step = pd.Timedelta(minutes=mins)
            inside = (agg["timestamp"] >= base.START) & (agg["timestamp"] < base.END)
            warm = agg["timestamp"] < base.START
            if (not inside.any() or (counts.loc[agg.loc[inside, "timestamp"]] != ratio).any()
                    or int(warm.sum()) < 250):
                raise ValueError(
                    f"UNAVAILABLE_INCOMPLETE_DERIVED_BARS: {symbol}/{timeframe}")
            frame = agg.loc[~((warm) & (counts.to_numpy() != ratio))].reset_index(drop=True)
            live = frame[(frame["timestamp"] >= base.START) & (frame["timestamp"] < base.END)]
            if (live["timestamp"].iloc[0] != base.START
                    or live["timestamp"].iloc[-1] != base.END-target_step
                    or not (live["timestamp"].diff().dropna() == target_step).all()):
                raise ValueError(f"UNAVAILABLE_DERIVED_FIVE_YEAR_GAPS: {symbol}/{timeframe}")
            digest = hashlib.sha256(pd.util.hash_pandas_object(
                frame, index=False).values.tobytes()).hexdigest()
            coverage.update({
                "timeframe": timeframe, "source_timeframe": base_tf,
                "resample_factor": ratio, "resampled_from_only_verified_ohlcv": True,
                "start_utc": base.START.isoformat(),
                "end_exclusive_utc": base.END.isoformat(),
                "bar_count": len(live),
                "warmup_bar_count": int((frame["timestamp"] < base.START).sum()),
                "ohlcv_sha256": digest,
                "actual_first_utc": live["timestamp"].iloc[0].isoformat(),
                "actual_last_utc": live["timestamp"].iloc[-1].isoformat(),
            })
        coverage["tradable_proxy"] = True
        return frame, coverage, market
    if timeframe != "1d":
        raise ValueError(f"UNAVAILABLE_5Y_INTRADAY: {symbol} {timeframe}; no verified source")
    # Fetch enough daily pre-window bars for 200-period indicators.
    # Exchange holidays are genuine gaps; do not manufacture fake candles.
    base.WARM = pd.Timestamp("2020-01-01", tz="UTC")
    # Yahoo lists the canonical USD/JPY feed as JPY=X. The alternate
    # USDJPY=X feed has inconsistent daily high/low in the sampled period;
    # prefer canonical JPY=X, never alter or synthesize source prices.
    source_symbol = "JPY=X" if symbol == "USDJPY=X" else symbol
    frame = base.yahoo_daily(source_symbol)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    fields = ["open", "high", "low", "close"]
    for col in fields:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    if frame[fields].isna().any().any() or (frame[fields] <= 0).any().any():
        raise ValueError(f"UNAVAILABLE_INVALID_YAHOO_OHLC: {symbol}")
    if (frame["high"] < frame[["open", "close", "low"]].max(axis=1)).any() or (
            frame["low"] > frame[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError(f"UNAVAILABLE_INVALID_YAHOO_RANGES: {symbol}")
    if "volume" not in frame:
        frame["volume"] = float("nan")
    else:
        frame["volume"] = pd.to_numeric(frame["volume"], errors="coerce")
    window = frame[(frame["timestamp"] >= base.START) & (frame["timestamp"] < base.END)]
    warm = frame[frame["timestamp"] < base.START]
    if (len(window) < 900 or len(warm) < 200
            or window["timestamp"].iloc[0] > base.START + pd.Timedelta(days=5)
            or window["timestamp"].iloc[-1] < base.END - pd.Timedelta(days=8)):
        raise ValueError(f"UNAVAILABLE_YAHOO_5Y_COVERAGE: {symbol} {len(window)} bars, {len(warm)} warm")
    dates = window["timestamp"]
    gaps = dates.diff()
    max_gap = gaps.max()
    if max_gap > pd.Timedelta(days=10):
        previous = dates.shift(1)
        long_indices = window.index[gaps > pd.Timedelta(days=10)]
        allowed_taiwan_lunar_holiday = (symbol == "^TWII" and all(
            1 <= dates.loc[i].month <= 3
            and 1 <= previous.loc[i].month <= 3
            and gaps.loc[i] <= pd.Timedelta(days=16)
            for i in long_indices))
        if not allowed_taiwan_lunar_holiday:
            raise ValueError(f"UNAVAILABLE_YAHOO_LONG_GAP: {symbol} {max_gap}")
        print("TAIWAN_LUNAR_NEW_YEAR_MARKET_CLOSURES", [
            {"from": str(previous.loc[i]), "to": str(dates.loc[i]),
             "days": str(gaps.loc[i])} for i in long_indices], flush=True)
    digest = hashlib.sha256(pd.util.hash_pandas_object(
        frame, index=False).values.tobytes()).hexdigest()
    coverage = {
        "source": "Yahoo Finance chart historical daily OHLC",
        "source_symbol": source_symbol, "symbol": symbol,
        "timeframe": timeframe, "start_utc": base.START.isoformat(),
        "end_exclusive_utc": base.END.isoformat(),
        "warmup_bar_count": len(warm), "bar_count": len(window),
        "actual_first_utc": window["timestamp"].iloc[0].isoformat(),
        "actual_last_utc": window["timestamp"].iloc[-1].isoformat(),
        "missing_or_irregular_intervals": None,
        "exchange_holidays_not_invented": True, "largest_calendar_gap": str(max_gap),
        "ohlcv_sha256": digest, "historical_data": True,
        "volume_available": bool(frame["volume"].fillna(0).gt(0).any()),
        "cost_model": "legacy Yahoo futures/FX model or explicitly hypothetical 10bps/index",
        "tradable_proxy": not market.startswith("Index"),
        "tradingview_run_verified": False, "pine_v6_parity_verified": False,
    }
    return frame, coverage, market


def load_legacy_definitions(filename: str, variables: tuple[str, ...],
                            functions: tuple[str, ...]) -> dict:
    """Load only definitions, not a legacy script's module-level download loop.

    The source is the existing repository's own Python, preserving rules.
    """
    source = (SRC / filename).read_text(encoding="utf-8")
    module = ast.parse(source, filename=filename)
    nodes = []
    for node in module.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id in variables
                   for t in node.targets):
                nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in functions:
            nodes.append(node)
    scope = {"np": np, "pd": pd, "base": base, "math": math}
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,
                        type_ignores=[])), filename, "exec"), scope)
    missing = [key for key in (*variables, *functions) if key not in scope]
    if missing:
        raise RuntimeError(f"Missing original strategy definitions {missing}")
    return scope


def stats(trades: list[dict], symbol: str, timeframe: str,
          family: str, strategy: str, exit_name: str, rule: str,
          digest: str, coverage: dict, market: str) -> list[dict]:
    # IS: only positions fully closed before the final OOS year.
    is_trades = [t for t in trades if pd.Timestamp(t["entry_time"]) < base.OOS
                 and pd.Timestamp(t["exit_time"]) < base.OOS]
    fs = base.formula_stats(is_trades)
    k = fs["kelly"]
    k = max(0., float(k)) if math.isfinite(k) else 0.
    wr = [float(t["R"]) for t in is_trades]
    wins = [r for r in wr if r > 0]
    losses = [-r for r in wr if r <= 0]
    b = ((sum(wins) / len(wins)) / (sum(losses) / len(losses))
         if wins and losses and sum(losses) > 0 else math.nan)
    p = len(wins) / len(wr) if wr else math.nan
    rows = []
    for label, frac in (("固定1R", .10), ("全凱利", k),
                        ("半凱利", k/2), ("四分之一凱利", k/4)):
        full, executed, is_exec, oos_exec, reasons, oosret = intraday.summarize_execution(
            trades, frac)
        rets = [float(t["R"]) for t in executed]
        win = [r for r in rets if r > 0]
        lose = [-r for r in rets if r <= 0]
        pf = sum(win) / sum(lose) if lose and sum(lose) > 0 else math.nan
        ratio = ((sum(win)/len(win))/(sum(lose)/len(lose))
                 if win and lose and sum(lose) > 0 else math.nan)
        rows.append({
            "來源": "新策略實測" if family == "new" else "舊策略重新實測",
            "市場": market, "商品": symbol, "可交易": coverage["tradable_proxy"],
            "策略分類": family, "策略": strategy, "策略規則": rule,
            "時區": timeframe, "出場方式": exit_name, "倉位法": label,
            "實際風險_pct": frac*100, "IS_Kelly_pct": k*100,
            "IS勝率_p": p, "IS失敗率_q": 1-p if math.isfinite(p) else math.nan,
            "IS平均贏虧比_b": b, "IS交易數": len(is_trades),
            "IS勝單數": len(wins), "IS敗單數": len(losses),
            "五年交易數": int(full[2]),
            "五年勝率_pct": len(win)/len(rets)*100 if rets else math.nan,
            "五年收益_pct": full[0], "五年最大回撤_pct": full[1],
            "五年獲利因子": pf, "五年盈虧比": ratio,
            "止盈出場數": int(reasons.get("止盈", 0)+reasons.get("固定止盈", 0)
                            +reasons.get("ATR移動止盈", 0)),
            "止損出場數": int(reasons.get("止損", 0)
                            +reasons.get("ATR移動止損", 0)),
            "OOS收益_pct": oosret, "OOS交易數": len(oos_exec),
            "資金停止": bool(full[3]), "資料完整": True,
            "OHLCV_SHA256": coverage["ohlcv_sha256"],
            "交易_SHA256": digest,
            "伯努利獨立同分布驗證": "未驗證（p/q是勝敗樣本估計）",
        })
    return rows


def atomic_write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        df.to_csv(tmp, index=False, encoding="utf-8-sig")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT", choices=list(SYMBOL_MARKET))
    parser.add_argument("--timeframe", required=True, choices=PERIODS)
    parser.add_argument("--family", required=True, choices=FAMILIES)
    args = parser.parse_args()
    name = (f"legacy_{args.symbol}_{args.timeframe}_{args.family}"
            if args.symbol == "BTCUSDT" and args.family != "new"
            else f"multi_{args.symbol}_{args.timeframe}_{args.family}")
    output = OUT / name
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / "manifest.json"
    # Each batch is independently idempotent. Check persisted checksums rather
    # than considering an incomplete CSV a completed batch.
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("status") == "complete":
            expected = data.get("ranking_sha256")
            rank = output / "ranking.csv"
            if rank.exists() and expected == hashlib.sha256(rank.read_bytes()).hexdigest():
                print("ALREADY_COMPLETE", name, flush=True)
                return

    raw, coverage, market = load_market_ohlcv(args.symbol, args.timeframe)
    execution_market = "Crypto futures" if market.startswith("Index") else market
    print("VALIDATED_FIVE_YEAR_SOURCE", json.dumps(coverage), flush=True)

    # Compute heavy OHLCV indicators exactly once per job; legacy simulators
    # otherwise recompute Supertrend repeatedly for each profit-taking variant.
    orig_indicators = base.indicators
    prepared = orig_indicators(raw)
    base.indicators = lambda _: prepared.copy(deep=False)
    if args.family == "original":
        tasks = [(s.replace("_TP2R","").replace("_TP3R",""), s, "", "")
                 for s, _ in base.STRATS]
        signal_fn = base.make_signals
        backtest_fn = exits.backtest
        modes = exits.MODES
    elif args.family == "compound":
        comp = load_legacy_definitions("five_year_compound_strategy_sweep.py",
                                       ("DEFINITIONS",), ("custom_signals",))
        tasks = [(s, s, v, "") for s, v in comp["DEFINITIONS"].items()]
        signal_fn = comp["custom_signals"]
        backtest_fn = exits.backtest
        modes = exits.MODES
    elif args.family == "fixed":
        fixed = load_legacy_definitions("five_year_low_drawdown_fixed_rr.py",
                                        ("RULES", "TP_RS"), ("signals", "run_bracket"))
        tasks = [(s, s, v, "") for s, v in fixed["RULES"].items()]
        signal_fn = None
        backtest_fn = fixed["run_bracket"]
        modes = [(f"固定止盈{tp:g}R", tp, None) for tp in fixed["TP_RS"]]
    else:
        new_rules = intraday.old
        tasks = [(s, s, v, "") for s, v in new_rules.RULES.items()]
        signal_fn = None
        backtest_fn = new_rules.run
        modes = [(f"固定止盈{tp:g}R", tp, None) for tp in new_rules.TP_RS]

    # Preserve the source's exact signals but compute each once per OHLCV
    # batch. Exit variants change stops/TP only; recomputing the same millions
    # of 1m signals nine times would waste hours without affecting results.
    signal_cache = {}
    if signal_fn is not None:
        def cached_signals(d, name):
            if name not in signal_cache:
                signal_cache[name] = signal_fn(d, name)
            return signal_cache[name]
        base.make_signals = cached_signals
    elif args.family == "fixed":
        fixed_scope = fixed["run_bracket"].__globals__
        source_fixed_signals = fixed_scope["signals"]
        def cached_fixed_signals(d, name):
            if name not in signal_cache:
                signal_cache[name] = source_fixed_signals(d, name)
            return signal_cache[name]
        fixed_scope["signals"] = cached_fixed_signals
    else:
        new_scope = new_rules.run.__globals__
        source_new_signals = new_scope["make_state"]
        def cached_new_signals(d, name):
            if name not in signal_cache:
                signal_cache[name] = source_new_signals(d, name)
            return signal_cache[name]
        new_scope["make_state"] = cached_new_signals

    trades_out = []
    rows = []
    statuses = []
    try:
        for display_name, input_name, rule, _ in tasks:
            if not coverage.get("volume_available", True) and (
                    "Volume" in display_name or "volume" in display_name):
                statuses.append({"strategy": display_name, "status": "unavailable_volume",
                                 "reason": "provider lacks historical volume"})
                print("UNAVAILABLE_VOLUME", args.symbol, display_name, flush=True)
                continue
            options = []
            for mode, tp, trail in modes:
                if args.family in ("fixed", "new"):
                    trades = backtest_fn(raw, execution_market, args.symbol,
                                         input_name, tp)
                else:
                    trades = backtest_fn(raw, execution_market, args.symbol,
                                         input_name, tp, trail)
                is_t = [t for t in trades
                        if pd.Timestamp(t["entry_time"]) < base.OOS
                        and pd.Timestamp(t["exit_time"]) < base.OOS]
                isret, isdd, _, _ = base.fixed_risk_stats(is_t, .10)
                options.append((mode, tp, trail, trades, is_t, isret, isdd))
                # Original family's distinct exit variants remain testable;
                # two-signal/fixed families select one by IS, like old scripts.
                if args.family == "original":
                    options[-1] = options[-1]  # explicit keep-all
            if args.family == "original":
                chosen = options
            else:
                eligible = [v for v in options if len(v[4]) >= 20 and v[5] > 0]
                if not eligible:
                    eligible = [v for v in options if v[5] > 0] or options
                chosen = [max(eligible, key=lambda v:
                              (v[5] / max(v[6], 1.), v[5], len(v[4])))]
            for mode, tp, trail, trades, _, _, _ in chosen:
                # Uniquely retain selected actual trade stream to prove counts
                # and give independent reconstruction of Bernoulli samples.
                tdf = pd.DataFrame([{
                    "策略": display_name, "出場方式": mode,
                    "entry_time": str(t["entry_time"]),
                    "exit_time": str(t["exit_time"]),
                    "R": t["R"], "reason": t["reason"],
                } for t in trades])
                payload = tdf.to_csv(index=False).encode("utf-8-sig")
                digest = hashlib.sha256(payload).hexdigest()
                trades_out.extend(tdf.to_dict("records"))
                rows.extend(stats(trades, args.symbol, args.timeframe,
                                  args.family, display_name, mode, rule,
                                  digest, coverage, market))
            statuses.append({"strategy": display_name, "status": "completed",
                             "tested_exit_count": len(options),
                             "saved_exit_count": len(chosen)})
            atomic_write_csv(pd.DataFrame(rows), output / "ranking.csv")
            atomic_write_csv(pd.DataFrame(trades_out), output / "trades.csv")
            (output / "checkpoint.json").write_text(json.dumps({
                "status": "partial", "family": args.family,
                "timeframe": args.timeframe, "strategies": statuses,
                "ranked_configs": len(rows),
                "saved_trades": len(trades_out)
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            print("DONE_STRATEGY", display_name, args.timeframe,
                  args.family, "ranked", len(rows), flush=True)
    finally:
        base.indicators = orig_indicators

    rank = output / "ranking.csv"
    csv_digest = hashlib.sha256(rank.read_bytes()).hexdigest()
    completed = {
        **coverage, "family": args.family, "status": "complete",
        "strategy_count": len(statuses), "completed": statuses,
        "ranking_rows": len(rows), "saved_trade_rows": len(trades_out),
        "ranking_sha256": csv_digest,
        "trades_sha256": hashlib.sha256((output/"trades.csv").read_bytes()).hexdigest(),
    }
    manifest.write_text(json.dumps(completed, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print("COMPLETE_VERIFIED", name, "rows", len(rows), flush=True)


if __name__ == "__main__":
    main()
