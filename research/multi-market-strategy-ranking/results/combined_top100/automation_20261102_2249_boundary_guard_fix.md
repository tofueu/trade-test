# Trade Test 2026-11-02 22:49 +08:00

## Actual change
- Updated `src/run_intraday.py` on the existing isolated branch, commit `050ca89009b2c66c65f2d457cf4586979f6e9d31`.
- Removed premature `in_window.empty` rejection before verified Binance daily archive boundary repair. Empty entire source still fails closed; five-year coverage and warm-up validation remain mandatory after attempted repair.
- No synthetic OHLCV; no legacy 1d rerun; no Jules; no new workflows; main untouched.

## Verification scope and limitations
- Confirmed exact old guard in GitHub source before patch; GitHub contents API accepted replacement.
- Container git network attempt failed: `Could not resolve host: github.com`. Therefore full Python compile, end-to-end SOL daily ZIP verification, and five-year signal reruns were **not performed**.
- New five-year strategy signal combinations: **0**. Old trade replay validations: **0**. New raw OHLCV SHA256 checks: **0**.
- completed/required: **unverified** pending per-key reconciliation of complete manifests, trade CSVs, source SHA and workflow artifacts.
- Previous 744 declared exit configurations, 296 saved, 448 without complete saved exit evidence are historical audit claims, **not** verified completed full five-year runs.
- Do not rerun old 31 strategies on 1d in any of the nine markets. New seven strategies 1d only if missing and genuine five-year data exist.

## Next executable checks
1. Obtain complete runner bytes in an environment that can compile them and run Python syntax checks.
2. Collect BTC 1m original+compound and ETH 1m/3m/5m artifact SHA and per-trade provenance, deduplicate by market/timeframe/family/exit.
3. Verify SOL genuine Binance ZIP archive continuity and provenance, then only run missing signals.
4. Update the two existing leaderboards only with verified results.

Rankings (unchanged):
- [38 family leaderboard](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)
