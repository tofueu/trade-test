# Trade Test — 2026-11-01 11:55 +08:00 — recovered combined artifact, independent SHA audit

## Source and actual execution
Downloaded existing GitHub Actions run [41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962) artifact **verified-multi-market-python-rankings**, artifact ID **12992239501**, 241,440,493 bytes, generated 2026-10-30. Locally opened its ZIP with Python `zipfile`, parsed all nested `manifest.json` and independently recalculated SHA256 over each nested `ranking.csv` and `trades.csv` using `hashlib.sha256`.

**70 of 70 complete manifests passed both internal CSV hashes: 140 of 140 file hash comparisons passed, zero mismatches.** This verifies preserved output files against manifests, not source OHLCV independently and not new strategy signals. The ZIP has 290 entries, 70 manifests and combined_top100 rankings. Existing combined aggregation has `status: partial`, not complete.

Manifest counts: ETHUSDT 48, BTCUSDT 6, ES=F 4, GC=F 4, NQ=F 4, SI=F 4; **no SOLUSDT, ^TWII or USDJPY=X complete manifests in this recovered artifact**. 70 manifests contain 562 completed strategy entries (not necessarily unique strategy×exit keys). Timeframe manifest counts: 1d 23; 4h 7; 12h 4; 15m 4; 1h 4; 1m 4; 2h 4; 30m 4; 3m 4; 5m 4; 6h 4; 8h 4. No 20m entries. Preserve old legacy 1d results and never rerun them.

## State distinctions
- GitHub artifact exists and ZIP downloaded: yes.
- Nested manifest status complete: 70.
- Nested rankings/trades SHA independently verified: 70 batches, 140 files.
- Original source OHLCV SHA independently verified: **0** in this run.
- New genuine OHLCV Python signal backtests in this run: **0**.
- Existing trade replay checks in this run: **0**.
- Total completed/required at market×timeframe×family×strategy×exit granularity: **unknown**; saved-exit and tested-exit counts differ, and historical snapshots are not equivalent to independently verified source replay.

## Ranking caveat and next executable repair
Recovered `combined_top100/top100_by_return.csv` includes XRPUSDT, which is out of the nine-market scope. It also contains legacy daily rows tagged `legacy_daily_snapshot_unreproduced`. Do not promote this combined historical leaderboard to fully verified nine-market Top100. Rebuild a nine-market-only derived ranking with >=70 trades, >100% return, actual risk <= IS Kelly, while preserving original evidence and checking duplicate strategy×exit keys. Bernoulli iid is unproven.

Priority: collect BTC 1m original/compound and ETH 1m/3m artifacts; independently validate source OHLCV SHA and run missing real-data 20m configurations, never rerun old 31 × 1d. Investigate SOL empty artifacts and genuine Binance daily gaps before retrying only missing configurations.

No Jules, no new workflow, no changes to main, no reruns. This report is a recovery/verification result, not a claim of full five-year completion.
