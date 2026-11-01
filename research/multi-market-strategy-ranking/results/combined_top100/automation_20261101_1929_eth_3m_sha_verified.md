# Trade Test 2026-11-01 19:29 (+08) — ETHUSDT 3m artifact independent verification

Scope: 9 specified markets × 17 specified timeframes; **no old-family 1d reruns**. No Jules, no new workflows, no main changes.

## Executed this run
Downloaded GitHub Actions run 41066783962 artifact `market-ETHUSDT-3m` (artifact ID 12988929734), independently processed with Python zipfile/tarfile/hashlib. Outer ZIP SHA256 `a53868d60ad92fb3711f66da0b446ea3a2a2f03b4b3eb55954533d2185cb34a1` matches GitHub's digest. Independently streamed SHA256 of all 8 internal CSVs and counted rows; all match each family manifest.

| family | strategies | ranking rows | trade rows | ranking SHA | trades SHA |
|---|---:|---:|---:|---|---|
| original | 8 | 288 | 1,954,098 | pass | pass |
| compound | 8 | 32 | 298,410 | pass | pass |
| fixed | 9 | 36 | 228,550 | pass | pass |
| new | 7 | 28 | 107,844 | pass | pass |
| **Total** | **32** | **384** | **2,588,902** | **4/4** | **4/4** |

All 4 manifests report status=complete, five-year window [2021-10-10, 2026-10-10), 876,480 ETHUSDT 3m candles, zero declared missing intervals, and OHLCV SHA256 `6a1331d4c7f0e4db35461a9fc6185bee01d32e781f826b1796234d2bb281d56e`. **OHLCV source bytes were not independently retrieved/rehashed**, so the OHLCV digest is a manifest claim only. No new strategy signals were run: **0 new five-year strategy×market×timeframe×exit combinations**; 0 trade replays. This was 8 existing CSV integrity checks, not a new backtest.

**Important deduplication**: original reports 9 tested/saved exits per strategy; compound reports 9 tested but only 1 saved; fixed/new report 5 tested but only 1 saved. Do not mark unsaved exits as fully archived. Ranking rows include additional variations; do not equate rows with unique completed strategy×exit keys. Old 1d remains excluded from reruns.

Next: download ETH 1m and 5m and repeat internal SHA verification; build cross-artifact unique-key inventory using manifest + ranking + trades and independently verify real five-year OHLCV before running missing 20m. If source is unavailable, mark unavailable rather than invent bars.

Existing historical leaderboards (not yet fully verified):
- [38 families](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)

No new validated leaderboard entries, no full completed/required claim, and iid is not proven.
