# Trade Test 2026-11-02 20:14 +08:00 — runner source audit

Scope: tofueu/trade-test, branch report/trade-test-multi-market-20261030. Read current run_intraday.py via authenticated GitHub connector. No strategy replay or OHLCV source verification was performed in this run.

## Newly confirmed code-level blocker
The repaired function restore_gap_klines_from_binance_daily_archive rejects requests if missing timestamps span more than 20 distinct days (len(days)>20), and also rejects over 24,000 missing candles. load_real_ohlcv invokes this function for missing warm-up and boundary data. Consequently, a cache missing over 20 days of warm-up/boundary data cannot be repaired by the current code, even if authentic Binance daily archives exist. This is a source-code finding, not proof that a particular SOL cache has that shape. The runner also requires warmup.timestamp.iloc[0] == warm_start and complete warm-up continuity.

The runner INTERVALS set contains 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d only; the requested 2m,10m,20m,45m,3h are absent from this particular runner. This does not establish absence from run_legacy_all_timeframes.py.

## Completion accounting
New five-year OHLCV strategy signal runs: 0. Existing trade replay: 0. New artifact SHA verification: 0. Existing prior 13 manifests/448 exits were not independently revalidated this run. Full completed/required cannot be established from the fetched runner alone. No claim of passing Bernoulli iid, Kelly, SOL source continuity, or all-market completion.

## Safe next execution
1. Compile complete current runner in Python after fetching it into the execution environment.
2. Obtain actual SOL cache and source receipts, determine exact missing timestamp set; do not widen repair limits without source-by-source receipts and explicit bounds.
3. Cross-check original manifest/ranking/trades per market × timeframe × family × exit, protect all old 1d from rerun.
4. Execute only proven missing configurations on verified five-year OHLCV, then regenerate both leaderboards.

Existing leaderboard links:
- [All strategy families](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)

No Jules, no new workflow, no main changes.
