# Trade Test 2026-11-01 21:20 +08 — ETHUSDT 1m existing artifact independent hash audit

Existing Run [41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962) artifact market-ETHUSDT-1m (ID 12993586056) was downloaded and Python zipfile/tarfile/hashlib streamed over the complete ZIP and its eight inner CSV files. Outer ZIP SHA256 `507ac6862784d2ea73dafa04b76d7aca86b984ee49b61f39128ea78d80885f31` matches GitHub's reported digest. All 8/8 CSV SHA256 values match the 4 manifest.json records; line counts excluding header match all declared ranking/trade counts.

| Family | Strategies | Ranking rows | Trade rows | Saved strategy×exit slots | Tested slots | Inner SHA |
|---|---:|---:|---:|---:|---:|---|
| original | 8 | 288 | 6,062,958 | 72 | 72 | 2/2 |
| compound | 8 | 32 | 913,615 | 8 | 72 | 2/2 |
| fixed | 9 | 36 | 763,312 | 9 | 45 | 2/2 |
| new | 7 | 28 | 348,893 | 7 | 35 | 2/2 |
| **Total** | **32** | **384** | **8,088,778** | **96** | **224** | **8/8** |

All four manifests declare status=complete, five-year [2021-10-10, 2026-10-10), 2,629,440 ETHUSDT 1m bars and zero gaps. The declared OHLCV SHA256 is `bf8ee513105eb6878e20d76dad66dbde52b79c7e33061dde817388d7282525a7`, **not independently checked against original market-data bytes**. Manifest completion and verified stored outputs are distinct from independently verified five-year OHLCV strategy recomputation. Saved slots must not be conflated with tested exits, and the count is not a cross-artifact deduplicated completion rate.

**New five-year OHLCV signal backtests this run: 0; existing-trade replays: 0; new inner CSV SHA validations: 8.** No missing strategy combination was rerun. No additional Kelly Top100 entry certified; iid remains unproven.

Old 31 strategies × 1d across all nine markets remain protected against reruns. Only nine specified markets and 17 specified timeframes are in scope; unavailable source data must never be synthesized. No Jules, new workflow, or main changes.

Next action: construct global market×timeframe×family×strategy×exit unique-key registry from saved manifests and rankings, preserving artifact-present, CSV-hash-verified, replay-verified and independently-source-verified as distinct statuses; then run only genuinely missing strategies against real complete OHLCV.

Historical (not yet fully certified) leaderboards:
- [38-family ranking](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
