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
FAMILIES = ("original", "compound", "fixed")
PERIODS = tuple(intraday.INTERVALS)


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
          digest: str, coverage: dict) -> list[dict]:
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
            "來源": "舊策略重新實測", "市場": "Crypto futures", "商品": symbol,
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
    parser.add_argument("--symbol", default="BTCUSDT", choices=["BTCUSDT"])
    parser.add_argument("--timeframe", required=True, choices=PERIODS)
    parser.add_argument("--family", required=True, choices=FAMILIES)
    args = parser.parse_args()
    name = f"legacy_{args.symbol}_{args.timeframe}_{args.family}"
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

    raw, coverage = intraday.load_real_ohlcv(args.symbol, args.timeframe)
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
    else:
        fixed = load_legacy_definitions("five_year_low_drawdown_fixed_rr.py",
                                        ("RULES", "TP_RS"), ("signals", "run_bracket"))
        tasks = [(s, s, v, "") for s, v in fixed["RULES"].items()]
        signal_fn = None
        backtest_fn = fixed["run_bracket"]
        modes = [(f"固定止盈{tp:g}R", tp, None) for tp in fixed["TP_RS"]]

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
    else:
        fixed_scope = fixed["run_bracket"].__globals__
        source_fixed_signals = fixed_scope["signals"]
        def cached_fixed_signals(d, name):
            if name not in signal_cache:
                signal_cache[name] = source_fixed_signals(d, name)
            return signal_cache[name]
        fixed_scope["signals"] = cached_fixed_signals

    trades_out = []
    rows = []
    statuses = []
    try:
        for display_name, input_name, rule, _ in tasks:
            options = []
            for mode, tp, trail in modes:
                if args.family == "fixed":
                    trades = backtest_fn(raw, "Crypto futures", args.symbol,
                                         input_name, tp)
                else:
                    trades = backtest_fn(raw, "Crypto futures", args.symbol,
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
                                  digest, coverage))
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
