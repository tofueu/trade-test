# EMA50_200 zero-trade investigation — 2026-11-26

Observed on the user's TradingView screenshot: no trades over 2019-09-08..2026-11-26 and a lookahead-bias warning.

Execution-port repairs:
- Read target_state[1] globally each bar instead of conditionally evaluating ta.change under a Pine v6 short-circuit condition.
- Disable calc_on_order_fills; only evaluate orders at confirmed closes for next-open fills.
- Queue the ATR-based initial protective stop with its entry, so it does not depend on a post-fill recalculation.
- Let strategy.entry reverse an opposite position without an additional strategy.close order.
- Retain EMA plots and add signal/filled-position Data Window diagnostics.

Preserved: EMA50/200 crossover state, original 10% initial-capital risk default, ATR14 x1.5, commission 0.10%, no explicit margin overrides (Pine v6 defaults still apply), no end date, no Python/main modifications. Existing TP input was already unused; fixed TP remains unimplemented.

Validation: source assertions and controlled state-transition fixture passed. This is not a Pine compiler or broker emulator. TradingView compilation/execution and historical performance parity are NOT TESTED. It is not proven that conditional-history calculation alone caused the user's zero trades. Default 100% margin can independently reject ATR-risk-sized entries. No margin or risk change was silently applied.

The current port's defaults still differ from the homepage's SOL3h rank1 configuration. No claim of reproducing the ranked return is made. Existing TV chart settings may override declaration defaults; use a separate new script/default settings for comparison. Existing alert snapshots do not auto-update.
