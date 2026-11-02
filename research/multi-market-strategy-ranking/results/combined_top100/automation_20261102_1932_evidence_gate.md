# Trade Test 2026-11-02 19:32 Asia/Taipei — evidence gate

## This run (no invented completion)
- New five-year real-OHLCV strategy-signal configurations: **0**.
- Old trade replay: **0**.
- New independent physical CSV SHA checks: **0**.
- New original-OHLCV independent SHA checks: **0**.
- Newly qualified Kelly Top100 entries: **0**.
- Verified global completed/required: **undetermined** (not zero; not a claimed completion).
- New Python execution: recalculated an evidence-only ledger from the existing 13-record SHA audit, without rerunning strategies.

## Verified historical evidence boundary
The previously preserved audit JSON `trade_test_20261102_1135_sha_audit.json` contains 13 records, with 744 claimed tested exits, 296 claimed saved exits, 448 exits lacking saved-output evidence, and 13,129,823 trade rows across the four priority artifacts (BTC 1m compound, ETH 1m/3m/5m). These are **artifact-level prior SHA audit assertions**, not independently validated OHLCV/signal recomputation. The 448 are **not** authorized rerun targets until per-exit IDs and ranking/trades are reconciled.

## Source inspection this run
Read current `research/multi-market-strategy-ranking/src/run_intraday.py` from `report/trade-test-multi-market-20261030`, blob SHA `405a3ce6fd7bc2ea871b85f35748b491bdb17293`.
- The warm-up/boundary repair, interior repair, and cache receipt logic are present in source.
- `restore_gap_klines_from_binance_daily_archive` rejects >20 distinct missing days and >24,000 interior missing bars; do not describe a five-year SOL data restoration as proven until actual archive retrieval, full timestamp coverage, and digest validation succeed.
- Full runner `py_compile` and end-to-end SOL download/backtest were **not performed** in this run: local runtime has no authenticated checkout and `git ls-remote https://github.com/tofueu/trade-test.git` failed DNS resolution. Connector source inspection is not a substitute for Python compilation.
- Runner `INTERVALS` is not the complete 17-period specification; the legacy timeframe runner must be assessed separately. No new timeframe was silently declared unavailable.

## Immutable constraints
Do not rerun any legacy 1d strategy in any of nine markets. Only incremental missing unique `market × timeframe × family × exit` keys, backed by real five-year OHLCV and trade provenance. Never infer OHLCV completeness from artifact digest alone. No Jules, new workflows, or main-branch changes.

## Next executable step
Recover the runner as an executable local file via authenticated GitHub checkout or connector-backed materialization, run `python -m py_compile` and targeted regression tests, then verify Binance SOL missing daily ZIP rows and five-year coverage before running any deduplicated missing signal configuration. Preserve both existing ranking CSVs unchanged until source evidence supports a rebuild.
