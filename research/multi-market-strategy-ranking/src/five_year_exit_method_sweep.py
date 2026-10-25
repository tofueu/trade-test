"""Compare take-profit/exit variants on the cached 5y multi-market dataset.

Entry signals and initial 1.5 ATR stop remain unchanged. Exit candidates are
selected only as research variants; no live trading is performed.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

import five_year_multi_market_kelly as base

ROOT = Path(__file__).resolve().parent
MODES = [
    ("訊號出場(無固定TP)", None, None),
    ("固定0.5R+訊號出場", 0.5, None),
    ("固定1R+訊號出場", 1.0, None),
    ("固定1.5R+訊號出場", 1.5, None),
    ("固定2R+訊號出場", 2.0, None),
    ("固定3R+訊號出場", 3.0, None),
    ("固定4R+訊號出場", 4.0, None),
    ("ATR移動止盈2x+訊號出場", None, 2.0),
    ("ATR移動止盈3x+訊號出場", None, 3.0),
]


def backtest(raw: pd.DataFrame, market: str, symbol: str, strategy: str,
             fixed_tp_r: float | None, trail_atr: float | None) -> list[dict]:
    d = base.indicators(raw)
    sig = base.make_signals(d, strategy)
    slip, fee = base.costs(market, symbol)
    opens, highs, lows, closes = (d[c].to_numpy() for c in ("open", "high", "low", "close"))
    atr = d.atr.to_numpy()
    ts = d.timestamp
    trades: list[dict] = []
    side = 0
    entry = stop = take = 0.0
    entry_i = 0
    best_fav = 0.0

    def slip_amt(px: float) -> float:
        return slip * abs(px) if market == "Crypto futures" else slip

    def close_trade(i: int, px: float, reason: str, *, open_position: bool = True) -> None:
        nonlocal side
        px_exec = px - side * slip_amt(px)
        risk = abs(entry - initial_stop)
        pnl = side * (px_exec - entry) - fee * (abs(entry) + abs(px_exec))
        trades.append({"entry_time": ts.iloc[entry_i], "exit_time": ts.iloc[i],
                       "side": side, "R": pnl / risk if risk else 0.0,
                       "reason": reason})
        side = 0

    initial_stop = 0.0
    for i in range(1, len(d)):
        if ts.iloc[i] < base.START:
            continue
        target = int(sig[i - 1])
        if side and target != side:
            # The prior completed candle's signal is known at this bar's open.
            close_trade(i, opens[i], "訊號出場")
        elif side:
            exit_px = None
            exit_reason = None
            if side == 1:
                if opens[i] <= stop or lows[i] <= stop:
                    exit_px = min(opens[i], stop)
                    exit_reason = ("ATR移動止盈" if trail_atr is not None and stop > entry else
                                   "ATR移動止損" if trail_atr is not None else "止損")
                elif fixed_tp_r is not None and (opens[i] >= take or highs[i] >= take):
                    exit_px, exit_reason = take, "止盈"
                best_fav = max(best_fav, highs[i])
            else:
                if opens[i] >= stop or highs[i] >= stop:
                    exit_px = max(opens[i], stop)
                    exit_reason = ("ATR移動止盈" if trail_atr is not None and stop < entry else
                                   "ATR移動止損" if trail_atr is not None else "止損")
                elif fixed_tp_r is not None and (opens[i] <= take or lows[i] <= take):
                    exit_px, exit_reason = take, "止盈"
                best_fav = min(best_fav, lows[i]) if best_fav else lows[i]
            if exit_px is not None:
                close_trade(i, exit_px, exit_reason or "止損")
            elif side and trail_atr is not None and np.isfinite(atr[i]) and atr[i] > 0:
                # Updated after this candle closes; it is active from the next bar.
                candidate = best_fav - side * trail_atr * atr[i]
                stop = max(stop, candidate) if side == 1 else min(stop, candidate)

        start_transition = ts.iloc[i] >= base.START and ts.iloc[i - 1] < base.START
        if (not side and target and
                (i == 1 or sig[i - 2] == 0 or target != int(sig[i - 2]) or start_transition) and
                np.isfinite(atr[i - 1]) and atr[i - 1] > 0):
            side = target
            entry_i = i
            entry = opens[i] + side * slip_amt(opens[i])
            dist = 1.5 * atr[i - 1]
            initial_stop = entry - side * dist
            stop = initial_stop
            take = entry + side * fixed_tp_r * dist if fixed_tp_r is not None else 0.0
            best_fav = entry
            slhit = lows[i] <= stop if side == 1 else highs[i] >= stop
            tphit = (fixed_tp_r is not None and
                     (highs[i] >= take if side == 1 else lows[i] <= take))
            if slhit:
                close_trade(i, min(opens[i], stop) if side == 1 else max(opens[i], stop), "止損")
            elif tphit:
                close_trade(i, take, "止盈")
            else:
                best_fav = max(best_fav, highs[i]) if side == 1 else min(best_fav, lows[i])
                # Current bar's favorable excursion only affects the next bar.
                if trail_atr is not None and np.isfinite(atr[i]) and atr[i] > 0:
                    candidate = best_fav - side * trail_atr * atr[i]
                    stop = max(stop, candidate) if side == 1 else min(stop, candidate)

    if side:
        px = closes[-1]
        px_exec = px - side * slip_amt(px)
        risk = abs(entry - initial_stop)
        pnl = side * (px_exec - entry) - fee * (abs(entry) + abs(px_exec))
        trades.append({"entry_time": ts.iloc[entry_i], "exit_time": ts.iloc[-1],
                       "side": side, "R": pnl / risk if risk else 0.0,
                       "reason": "期末平倉"})
    return trades


def size_metrics(trades: list[dict], fraction: float) -> tuple[float, float, int, bool]:
    return base.fixed_risk_stats(trades, fraction)


def main() -> None:
    instruments = []
    for s in base.CRYPTO:
        instruments.append(("Crypto futures", s, s, lambda s=s: base.binance_daily(s)))
    for s, (name, _) in base.FX.items():
        instruments.append(("FX", s, name, lambda s=s: base.yahoo_daily(s)))
    for s, (name, _, _) in base.FUTURES.items():
        instruments.append(("Traditional futures", s, name, lambda s=s: base.yahoo_daily(s)))

    rows = []
    ledger = []
    for market, symbol, label, loader in instruments:
        raw = loader().dropna(subset=["open", "high", "low", "close"]).copy()
        raw["timestamp"] = pd.to_datetime(raw.timestamp, utc=True)
        raw = raw.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
        for strategy, _legacy_tp in base.STRATS:
            for mode, tp_r, trail in MODES:
                trades = backtest(raw, market, symbol, strategy, tp_r, trail)
                if not trades:
                    continue
                rs = [float(t["R"]) for t in trades]
                p = sum(r > 0 for r in rs) / len(rs)
                win_r = [r for r in rs if r > 0]
                loss_r = [-r for r in rs if r <= 0]
                avg_win = float(np.mean(win_r)) if win_r else float("nan")
                avg_loss = float(np.mean(loss_r)) if loss_r else float("nan")
                b = avg_win / avg_loss if win_r and loss_r and avg_loss else float("nan")
                k = (b * p - (1-p)) / b if math.isfinite(b) and b > 0 else 0.0
                is_trades = [t for t in trades if pd.Timestamp(t["entry_time"]) < base.OOS]
                oos_trades = [t for t in trades if pd.Timestamp(t["entry_time"]) >= base.OOS]
                isfm = base.formula_stats(is_trades)
                oosfm = base.formula_stats(oos_trades)
                is_k = max(0.0, isfm["kelly"]) if math.isfinite(isfm["kelly"]) else 0.0
                modes = [
                    ("固定1R", base.FIXED_RISK, base.FIXED_RISK),
                    ("全凱利", max(0.0, k), is_k),
                    ("半凱利", max(0.0, k/2), is_k/2),
                    ("四分之一凱利", max(0.0, k/4), is_k/4),
                ]
                counts = {reason: sum(t["reason"] == reason for t in trades) for reason in
                          ["止盈", "止損", "訊號出場", "ATR移動止盈", "ATR移動止損", "期末平倉"]}
                for t in trades:
                    ledger.append({"市場":market,"商品":label,"代碼":symbol,
                                   "訊號策略":strategy.replace("_TP2R", "").replace("_TP3R", ""),
                                   "出場方式":mode, **t})
                for alloc, f, is_f in modes:
                    ret, dd, done, halted = size_metrics(trades, f)
                    oosret, oosdd, oosdone, ooshalted = size_metrics(oos_trades, is_f)
                    rows.append({
                        "倉位方法":alloc,"市場":market,"商品":label,"代碼":symbol,
                        "訊號策略":strategy.replace("_TP2R", "").replace("_TP3R", ""),
                        "出場方式":mode,"固定TP_R":tp_r,"ATR追蹤倍數":trail,
                        "交易數":len(trades),"已完成交易數":done,"止盈數":counts["止盈"],
                        "止損數":counts["止損"],"訊號出場數":counts["訊號出場"],
                        "ATR移動止盈數":counts["ATR移動止盈"],"ATR移動止損數":counts["ATR移動止損"],
                        "期末平倉數":counts["期末平倉"],"勝率":p,"EV_R":float(np.mean(rs)),
                        "五年收益_pct":ret,"最大回撤_pct":dd,"風險比例_pct":f*100,
                        "IS交易數":isfm["n"],"IS凱利比例_pct":is_k*100,
                        "OOS交易數":oosfm["n"],"OOS勝率":oosfm["p"],
                        "OOS_EV_R":oosfm["ev"],"OOS收益_pct":oosret,"OOS最大回撤_pct":oosdd,
                        "OOS資金不足停止":ooshalted,"資金不足停止":halted,
                    })
        print(f"DONE {market} {label}", flush=True)

    df = pd.DataFrame(rows).sort_values("五年收益_pct", ascending=False).reset_index(drop=True)
    df.insert(0, "五年收益排名", np.arange(1, len(df)+1))
    df.to_csv(ROOT / "five_year_exit_variants_all_ranked.csv", index=False)
    df[df["交易數"] > 50].sort_values("五年收益_pct", ascending=False).reset_index(drop=True).assign(
        **{"50筆以上排名": lambda x: np.arange(1, len(x)+1)}
    ).to_csv(ROOT / "five_year_exit_variants_over50_ranked.csv", index=False)
    pd.DataFrame(ledger).to_csv(ROOT / "five_year_exit_variants_ledger.csv", index=False)
    df.head(50).to_csv(ROOT / "five_year_exit_variants_top50.csv", index=False)
    print("TOTAL", len(df), "OVER50", int((df["交易數"] > 50).sum()), flush=True)
    print(df.head(50)[["五年收益排名","倉位方法","市場","商品","訊號策略","出場方式",
                       "交易數","止盈數","訊號出場數","ATR移動止盈數","五年收益_pct",
                       "最大回撤_pct","OOS收益_pct","OOS交易數"]].to_string(index=False))


if __name__ == "__main__":
    main()
