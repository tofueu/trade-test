# Trade Test 2026-11-01 19:45 (+08) — ETHUSDT 5m existing artifact verification

Scope remains 9 specified markets and 17 timeframes; old 31 strategies × 1d in all 9 markets are protected from reruns. No Jules, new workflow, or main change.

## Actually executed
Downloaded existing Actions run 41066783962 artifact `market-ETHUSDT-5m` (ID 12986299665) and used Python zipfile/tarfile/hashlib to stream and hash its contents. Outer ZIP SHA256 `2039fd39c0b82ce4da8a2aa4f94cf9e800f02d6ea9930adf2b924d40f7f27ae6` matches the GitHub artifact digest. All 4 manifests say `status=complete`; all 8 internal ranking/trades CSV SHA256 values match their manifest declarations. Row counts exclude headers.

| Family | Strategies | Ranking rows | Trade rows | CSV SHA |
|---|---:|---:|---:|---|
| original | 8 | 288 | 1,159,263 | 2/2 pass |
| compound | 8 | 32 | 177,043 | 2/2 pass |
| fixed | 9 | 36 | 127,932 | 2/2 pass |
| new | 7 | 28 | 63,319 | 2/2 pass |
| Total | 32 | 384 | 1,527,557 | 8/8 pass |

All manifests declare [2021-10-10, 2026-10-10), 525,888 ETHUSDT 5m bars, zero missing/irregular intervals and OHLCV SHA256 `fc230732cd7d7b6756e5b8cc4dbaf44ed6f54ef710a3fc5304b05fcfde8851bc`. This OHLCV hash is **not independently verified against source bytes**. `complete` is the artifact's claimed status, not a final independent source-data certification.

Original saves 9 exits per strategy; compound tests 9 but saves 1, fixed/new test 5 but save 1. Ranking rows are not interchangeable with unique strategy×exit completed configurations.

**New five-year OHLCV signal backtests this run: 0. Old-trade replays: 0. Existing CSV SHA checks: 8.** No missing configuration was rerun. No new Top100 entries certified. Overall completed/required remains unknown pending cross-artifact key-level reconciliation; iid not proven.

Next: recover ETHUSDT 1m artifact and verify its internal SHA; reconcile all saved strategy×exit keys, then attempt only genuinely missing combinations with verified five-year real OHLCV. Do not rerun legacy 1d or fabricate non-crypto minute candles.

Historical leaderboards (not fully certified):
- [All 38 families](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
