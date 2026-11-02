# Trade Test 2026-11-02 11:35 +08:00 — priority artifacts independently verified

This run downloaded four previously pending GitHub Actions artifact ZIPs and independently streamed SHA256 verification of the contained ranking.csv and trades.csv against each manifest.json.

- BTCUSDT 1m compound: artifact 12989801317, one family.
- ETHUSDT 1m: artifact 12993586056, four families (original, compound, fixed, new).
- ETHUSDT 3m: artifact 12988929734, four families.
- ETHUSDT 5m: artifact 12986299665, four families.
- **13 manifest-complete family/timeframe records, 26/26 ranking/trade CSV SHA256 checks passed, 13,129,823 saved trade rows.**
- 104 strategy-family/timeframe entries; 744 exit variants declared tested, but only 296 exit variants declared saved. These are not 744 independently verified exit trade files.
- All 13 manifests declare the five-year interval 2021-10-10 to 2026-10-10 UTC, zero missing/irregular bars and an OHLCV SHA256. The original OHLCV bytes were **not independently re-downloaded or verified**.
- Distinguish statuses: artifacts independently verified (CSV integrity), trade replay not performed, new raw-OHLCV strategy signal backtests **0**, new original-market OHLCV SHA verification **0**.
- Prior BTC 1m original artifact was independently verified in prior report (not re-run here).
- Do not rerun any old strategy 1d, do not dispatch Jules, do not create workflows, do not modify main.
- Overall completed/required remains unverified until all Git manifests and Actions artifacts are merged by market/timeframe/family/strategy/exit key.
- Next actionable step: merge the 13 records with existing Git manifests, inspect exit-level ranking identifiers and preserve only SHA-verified rows; investigate SOL gaps before any missing-configuration rerun.

Ranking references (historical, not regenerated this run):
- [All 38 families](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
