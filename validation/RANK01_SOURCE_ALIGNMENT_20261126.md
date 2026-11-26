# Rank 1 source/configuration alignment — 2026-11-26

The previous port still used a BTC daily example/default risk 10%, ta.atr (Wilder SMA-seeded RMA), 0.10% commission approximation, all available history, and Pine v6's default 100% margin checks. A trading/display repair did not make that configuration equal to the ranked SOL3h strategy. The user's TV result of 1 trade and +25.89% is not a valid reproduction of the rank 1 row.

Restored from saved ranking evidence:
- Binance USD-M SOLUSDT, 3h; initial capital 10,000.
- EMA50/200 crossover state, no fixed TP, initial 1.5 ATR14 stop.
- Fixed initial-capital full-Kelly risk fraction 13.67442526787219%, not compounded.
- pandas adjust=False EMA/ATR seeds from 2021-09-01; minimum 250 warm-up bars.
- Next-open signal execution; no same-direction re-entry after a stop until a new state.
- No notional margin/liquidation simulation in the original Python; explicit Pine margin_long=0/margin_short=0 reflects THAT RESEARCH ASSUMPTION. It is not an exchange leverage setting and is not a recommendation for real trading.
- Python original costs 0.05% price-adverse slippage plus 0.05% fee per side. Pine keeps actual fee 0.05%, tick slippage 0 because a fixed tick slippage cannot exactly reproduce a price percentage.
- No expiry. For benchmark parity use entry period 2021-10-10 <= t < 2026-10-10 UTC; later trades will change totals. Python liquidates an open position at its historical dataset end, which a live no-expiry Pine need not do.

Verification actually run:
- Existing cached hourly CSV hash matches its archive restoration receipt.
- Resampled 3h dataframe fingerprint differs from the older manifest; timestamp-unit and round-trip CSV parser checks did not reconcile it. Cause remains unresolved; no data was altered to force a match.
- Despite the fingerprint discrepancy, unchanged Python functions reproduced all 85 saved trade entry/exit times and per-trade R values (1e-10 tolerance), return +2264.1583629955517%, closed-trade equity max drawdown 84.69248985082334%.
- Translation of Pine recursive EMA/ATR formulas and state transitions matched original pandas indicators/signals on the cached bars.
- Cost-only sensitivity measured in Python, NOT TV: zero slippage +0.05% fee -> 85 trades,+2287.54309717349%; fee0.10% approximation ->85 trades,+2247.6022408929152%. These are not TradingView performance results or optimized strategy parameters.

NOT VERIFIED: Pine compilation, TradingView emulator fills, real-price feed parity, +/-5% TV return/trade-count tolerance. Intrabar TV drawdown differs in definition from Python closed-trade drawdown. Do not claim identical returns or assume a guarantee based on Python replay.

Existing TradingView chart properties and alert snapshots do not auto-update. Load this as a new script/default properties for testing. Compare BINANCE:SOLUSDT.P 3h with complete warm-up history and equal window. Existing order-routing code is independent and was not modified.
