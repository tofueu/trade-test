# Trade Test 2026-11-02 21:12 Asia/Taipei — boundary guard audit

## Verified source
- Branch: `report/trade-test-multi-market-20261030`
- File: `research/multi-market-strategy-ranking/src/run_intraday.py`
- Git blob SHA: `405a3ce6fd7bc2ea871b85f35748b491bdb17293`
- GitHub connector fetched complete UTF-8 source (458 lines). Local `git ls-remote` failed DNS: `Could not resolve host: github.com`.

## Newly isolated control-flow defect
At lines 214–216, `in_window.empty` raises `RuntimeError("Five-year historical coverage empty; no qualified ranking")` **before** lines 219–225 can attempt boundary repair from verified Binance daily ZIP. Thus a cache with only warm-up bars, or an incomplete source window with no rows inside START..END, is rejected without attempting the intended verified boundary repair. This is a source-code finding, not proof that SOL actually triggers this condition.

At lines 135–142, missing boundary timestamps are appended to the `missing` list **after** the interior 24,000-bar cap at lines 132–134; the 20-day cap at lines 146–148 still applies. This means boundary restoration limits are not symmetric with interior restoration limits. Do not blindly raise limits or fabricate candles; inspect actual missing timestamps and original daily ZIP receipts first.

## Actual execution and verification this round
- Newly computed genuine five-year strategy signal configurations: **0**.
- Existing trade replay validations: **0**.
- New raw OHLCV SHA validations: **0**.
- Existing artifact coverage: 744 tested exit variants, 296 saved, 448 lacking independent saved-exit evidence (prior reported aggregate only; not revalidated this round).
- All-market completed/required: **not established**; old 31 strategies × 1d on all nine markets must remain excluded from reruns.
- SOL five-year end-to-end validation: **not done**; no original archive bytes available in local runtime.
- Full Python compile: **not done**; local repository checkout blocked by DNS; connector text inspection is not equivalent to compile.

## Incremental next action
1. Obtain source via an executable Python-capable environment or verified checkout and run `python -m py_compile` on the exact blob.
2. Add a focused test with an empty five-year window and existing warm-up rows, checking that boundary recovery is attempted *before* rejecting; ensure the recovery still fails closed for absent real ZIP rows.
3. Retrieve SOL exact missing timestamps and real Binance daily ZIP receipts; validate every recovered OHLCV row, monotonic UTC timestamps, continuous 1m/5m coverage, and source SHA256 before any new strategy run.
4. Reconcile manifest `status=complete`, trade CSV, ranking, SHA and GitHub artifacts using market × timeframe × family × exit ID; do not rerun any evidenced complete key or old daily strategies.
5. Keep the 38-family ranking and Kelly-constrained Top100 unchanged until new independently verified results exist.

No Jules, no workflow additions, no main branch changes. This report is a source audit, not a new backtest.