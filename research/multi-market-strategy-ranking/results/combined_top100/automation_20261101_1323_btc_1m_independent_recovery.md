# Trade Test — 2026-11-01 13:23 +08 — BTC 1m original / compound independent recovery

## Actual work
Downloaded **existing** artifacts from [Run 41064675326](https://github.com/tofueu/trade-test/actions/runs/41064675326), without rerunning any strategies:
- `legacy_BTCUSDT_1m_original` artifact **12990135479** (112,080,486 bytes on GitHub).
- `legacy_BTCUSDT_1m_compound` artifact **12989801317** (16,555,494 bytes on GitHub).

Opened both ZIPs with Python `zipfile`, parsed `manifest.json`, independently streamed/decompressed `ranking.csv` and `trades.csv` through `hashlib.sha256`, and parsed ranking rows with `csv.DictReader`.

## Independently verified inner SHA256
| Family | ranking.csv SHA256 | trades.csv SHA256 | manifest matches |
|---|---|---|---|
| original | `7e9097fca05cdcb7e74a1532c10108c433255b80459b27127b24fcbe51e61217` | `2ed4721adbfa5b48e379fd8af2e45fd73dd7b099e1a484d5ada28b1d0e79a473` | YES |
| compound | `182cfd26ee03c9cb392bc2a617c968fda5c09a9a69f751d1a9e2db8706baaccc` | `42552850f17bd33ef91739da3ad1c0688ef1a560516851558860d9b2a8c49579` | YES |

Both manifests are `status=complete` for BTCUSDT 1m, 2021-10-10 inclusive through 2026-10-10 exclusive, 2,629,440 declared candles, zero declared missing intervals, common **manifest-declared** source OHLCV SHA `189c4856bba7a5e053aca8d2f4fc08eb9a2ddbede15c766051e5e5628d57b442`. Source OHLCV was **not independently downloaded or rehashed**, so source verification remains pending.

## Strategy / exit inventory and leaderboard eligibility
- Original: 8 strategies, 9 tested/saved exits per strategy; ranking.csv 288 rows (8 strategies × 9 exits × 4 position methods), trades.csv 6,222,051 declared rows. All 288 ranking rows have `IS_Kelly_pct=0.0`; 216 show zero trades, and remaining 72 have only 5–12 or similarly low trades. **Zero** ranking rows meet >=70 trades, >100% return and actual risk <= IS Kelly.
- Compound: 8 strategies, 9 tested exits per strategy but **only 1 saved exit per strategy** in the manifest; ranking.csv 32 rows (8 strategies × 1 saved exit × 4 position methods), trades.csv 924,586 declared rows. All 32 ranking rows have `IS_Kelly_pct=0.0`; 24 have zero trades and remaining 8 have 5–13 trades. **Zero** ranking rows qualify for the requested Kelly Top100.
- The two families must be preserved as existing results; `tested_exit_count` is not the same as `saved_exit_count`. Do not count 9 compound exits as 9 individually persisted full-result configurations without evidence.

## Precise completion state
- GitHub artifacts present and retrieved: **2**.
- Complete manifests: **2**.
- Independently verified inner ranking/trades CSV SHA256: **4/4**.
- Independently verified original OHLCV SHA256: **0**.
- Newly computed genuine five-year strategy signals: **0**.
- Old trade replay this run: **0**.
- New eligible Top100 rows from these two artifact rankings: **0**.
- Full market×timeframe×strategy×exit completion ratio: **unknown**, pending reconciliation of all artifacts and original source data.

**Important:** The 6,222,051 and 924,586 figures are manifest-declared saved trade row counts, not independently recounted this run. The GitHub outer artifact digest is not used as a substitute for independently verified inner CSV hashes.

## Next executable repair
Recover ETH 1m/3m/5m, reconcile all saved-exit keys with existing complete manifests and preserve old 31×1d. Independently rehash raw OHLCV before promoting these batches to fully source-verified. For missing 20m only, use contiguous genuine 5m candles; mark unavailable when data cannot be verified. No Jules, new workflows, reruns, or main changes.
