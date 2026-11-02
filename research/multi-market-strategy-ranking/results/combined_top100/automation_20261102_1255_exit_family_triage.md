# Trade Test 2026-11-02 12:55 +08:00 — exit provenance triage (incremental)

Reconciled the prior verified 13-record SHA audit JSON against the 12:03 Git report. **No new OHLCV signal backtest was executed**. This is a new family-level classification of the 448 manifest-declared tested-but-unsaved exit variants, not a new completion claim.

| Family | Manifests | Tested exits | Saved exits | Unsaved exit variants |
|---|---:|---:|---:|---:|
| compound | 4 | 288 | 32 | 256 |
| fixed | 3 | 135 | 27 | 108 |
| new | 3 | 105 | 21 | 84 |
| original | 3 | 216 | 216 | 0 |
| **Total** | **13** | **744** | **296** | **448** |

Scope: BTCUSDT 1m compound; ETHUSDT 1m, 3m, 5m compound/fixed/new/original. Four artifact IDs: 12989801317, 12993586056, 12988929734, 12986299665. Prior SHA audit records say all 26 ranking/trades CSV hashes match and contain 13,129,823 trade rows; **hashes were not independently recomputed this run**. This audit excludes BTC 1m original (previously verified separately), other Git manifests, and any as-yet-uncollected artifacts.

**Important interpretation:** The 448 are manifest-declared unsaved exit variants, **not 448 missing signal backtests**. Original-family variants for ETH 1m/3m/5m have 0 such unsaved declarations. Need exit-level ranking and trade provenance before determining any rerun. No assumption of five-year OHLCV authenticity from CSV integrity alone.

New OHLCV signal combinations: **0**. Old trade replays: **0**. New independent SHA validations: **0**. Completed/required for 9 markets × 17 timeframes × 38 strategies × exits: **unverified**; unavailable five-year sources are not invented. SOL gap repair remains pending actual UTC missing timestamps and original Binance archive verification.

Next action: retrieve and inspect per-exit ranking/trades headers for these four artifacts, then cross-reference with Git manifests and BTC original, classify keys as artifact-only / SHA-verified / replay-verified / five-year-signal-verified, and only rerun genuinely missing signal configurations. Legacy strategies on all nine markets at 1d remain protected; no Jules, no new workflows, no main modification.

Existing rankings unchanged:
- [38 families](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
