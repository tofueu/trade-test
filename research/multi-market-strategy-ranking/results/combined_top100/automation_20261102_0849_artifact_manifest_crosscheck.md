# Trade Test 2026-11-02 08:49 Asia/Taipei — Git tree and Actions cross-check

## Verified reads
- Git tree of `report/trade-test-multi-market-20261030` returned non-truncated, with **30** `results/all_timeframes/**/manifest.json` files (6 legacy BTC, 24 multi-market).
- `results/combined_top100/latest_verification_manifest.json` declares `status=partial`, `verified_multi_asset_batch_count=24`, `completed_legacy_timeframe_family_batches=6`, `required_legacy_timeframe_family_batches=36`. These are **historical self-reported counts**, not an independent byte-level SHA validation this round.
- Run 41064675326 artifact list includes `legacy_BTCUSDT_1m_original` (ID 12990135479; 112080486 bytes; sha256 54324a419f95bbd31c4da3dd2ab50c800334e4cb587033ba3339ad637e5a98bc) and `legacy_BTCUSDT_1m_compound` (ID 12989801317; 16555494 bytes; sha256 f7389fdbf4f194e3611cc79d23b19357f5f8985d40fc603f1bfeedf94380b472).
- Run 41066783962 lists ETH 1m (12993586056, sha256 507ac6862784d2ea73dafa04b76d7aca86b984ee49b61f39128ea78d80885f31), 3m (12988929734, sha256 a53868d60ad92fb3711f66da0b446ea3a2a2f03b4b3eb55954533d2185cb34a1), 5m (12986299665, sha256 2039fd39c0b82ce4da8a2aa4f94cf9e800f02d6ea9930adf2b924d40f7f27ae6). These are GitHub-reported digests, **not independently checked against downloaded ZIP bytes**.
- Read `multi_ETHUSDT_1d_new/manifest.json`: status complete, 1826 daily candles, 0 irregular intervals, 7 named strategies, `tested_exit_count=5` and `saved_exit_count=1` per strategy, ranking_rows=28, saved_trade_rows=210. Thus **35 tested exits cannot be treated as 35 separately persisted exit-level trade histories**. Keep original daily result, do not rerun.
- Actual runner path is `research/multi-market-strategy-ranking/src/run_intraday.py`. Its `load_real_ohlcv` branch uses `cache_hit`, and previously observed gap-repair guard is conditional on `not cache_hit`; this is a repair-path limitation, not proof of the specific SOL failure cause.

## New five-year signal tests / replays / SHA
- New genuine OHLCV strategy signal configurations: **0**
- Historical trade replay verifications: **0**
- Independently validated downloaded artifact SHA256: **0**
- Newly repaired SOL gaps: **0**
- Full asset×timeframe×family×exit completed/required: **not yet verified**.

## Next executable work
1. Download the five priority ZIP artifacts and verify their actual bytes against the listed digests, then unpack and validate internal manifest/rankings/trades.
2. Build deduplication by `market,timeframe,family,strategy,exit`, keeping existing legacy 1d immutable.
3. Diagnose SOL gaps by actual UTC timestamps and repair only with verified real Binance daily ZIP rows; do not synthesize prices.
4. Run only missing five-year strategy configurations after historical data and output SHA checks.
5. Refresh both historical all-38 and strict >=70 trades, >100% return, actual risk <= IS Kelly Top100 only from verified evidence. Bernoulli iid not established.

No Jules, no new workflows, no main branch modifications. This report is an evidence checkpoint, not a claim of completed backtesting.
