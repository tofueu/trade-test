# Trade Test 2026-11-02 12:03 +08:00 — incremental saved-exit coverage audit

This run re-read the existing 11:35 SHA audit JSON (13 manifest records, four artifact ZIPs) and used Python to aggregate **tested vs saved exit variants**, without rerunning previously completed strategies.

| Market / timeframe | Manifest families | Strategy entries | Tested exits (declared) | Saved exits (declared, CSV SHA previously checked) | Tested but not saved |
|---|---:|---:|---:|---:|---:|
| BTCUSDT 1m compound | 1 | 8 | 72 | 8 | 64 |
| ETHUSDT 1m | 4 | 32 | 224 | 96 | 128 |
| ETHUSDT 3m | 4 | 32 | 224 | 96 | 128 |
| ETHUSDT 5m | 4 | 32 | 224 | 96 | 128 |
| **Total** | **13** | **104** | **744** | **296** | **448** |

These counts are **manifest-declared**. The previous run verified 26 CSV SHA256 values; this run did not repeat that verification. The 448 unsaved variants must NOT be counted as independently verified trade-detail configurations, nor assumed to require strategy signal reruns: first inspect the ranking and source artifacts for exit-level trade provenance, and only then determine if missing outputs require an incremental run.

**Run-specific activity:** Python aggregation of 13 existing audit records; new five-year OHLCV strategy-signal combinations **0**; trade replays **0**; newly independently verified CSV SHA **0**; OHLCV independent SHA **0**. Overall completed/required remains unverified. Existing old-strategy 1d across all nine markets is protected from rerun. SOL 4h remains blocked pending actual UTC gap identification and Binance archive OHLCV validation. Do not fabricate unavailable bars.

**Next executable action:** derive unique market/timeframe/family/strategy/exit keys from manifest and CSV ranking columns; reconcile all Git and Actions artifacts (including BTC 1m original), and mark missing saved-exit provenance separately from truly unexecuted strategy signals. No Jules, no new workflow, no main changes.

Historical rankings (unchanged):
- [38-family leaderboard](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
