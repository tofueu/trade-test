# Current status and acceptance plan

## Published state
Remote PR #9 remains the audited Draft PR. Local Jules claims of 33 validated 70+ candidates and 43 pytest passes are not accepted until their files and SHA are visible at the remote PR head.

## Not accepted
A local-only ranking, a static parity test, or `TV_UNVERIFIED` Pine code is not a final deliverable. Real TradingView compilation/run must remain unverified unless direct evidence exists.

## Required next delivery
1. Use supported publishing to update this same branch with the validated ranking CSV/MD and validator.
2. Re-run the validator and full pytest, reporting retained/excluded counts.
3. For every ranking row include five-year dates, source, fees/slippage, trades, total return, CAGR, max drawdown, win rate, PF, IS Kelly, OOS metrics, rules and Pine validation state.
4. Preserve the existing 9,556 results; no live trade, main modification, merge or invented TradingView result.
