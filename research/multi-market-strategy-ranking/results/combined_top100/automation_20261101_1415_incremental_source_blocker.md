# Trade Test — 2026-11-01 14:15 +08 — incremental execution and source audit

## Verified in this run
- Read existing branch `report/trade-test-multi-market-20261030` and previous BTC 1m SHA audit. BTC original/compound previously independently verified four inner CSV SHA values; **not re-run**.
- Queried existing Actions run [41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962/artifacts): ETHUSDT 1m artifact 12993586056 (151493344 bytes), ETHUSDT 3m artifact 12988929734 (49106611 bytes), ETHUSDT 5m artifact 12986299665 (28902635 bytes), all `expired=false` at query time. These are **presence only**; this run did not download or independently hash their inner contents.
- Ran actual Python `socket.getaddrinfo(host,443)` for `data.binance.vision` and `raw.githubusercontent.com`; both failed `gaierror [Errno -3] Temporary failure in name resolution`. No five-year real OHLCV downloaded, no source SHA independently checked.
- `/mnt/data` file scan (max depth 2) returned no locally available source files. No reproducible strategy signal run possible with the available data in this environment. A direct `tools/run_legacy_all_timeframes.py` fetch on this branch returned 404; repository root lists only `.github`, `.gitignore`, `README.md`, `research`, so code location must be resolved within research before local execution.

## Strict metrics for this run
- Newly computed five-year raw OHLCV strategy signal configurations: **0**.
- Previously saved trade replay validations: **0**.
- New independently verified inner CSV SHA256: **0**.
- Newly independently verified source OHLCV SHA256: **0**.
- New complete strategy×market×timeframe×exit keys: **0**.
- Overall verified completed/required ratio: **unknown**; 612 family-level cells and 138/188 prior batch inventories are not strategy-level completion counts.
- Two leaderboard CSVs unchanged; neither promoted to fully verified.
- Existing 31 legacy strategies × nine markets × 1d are protected against re-execution; no reruns issued.

## Concrete next repair
1. Resolve the real code path under `research/`, then retrieve the existing runner and manifest schemas.
2. Retrieve ETH 1m/3m/5m artifacts through a container-accessible channel, stream ZIP/TAR, independently compare inner ranking/trades hashes to manifests and record per strategy/exit saved keys. Existing outer GitHub digest is not sufficient.
3. Recover **real** five-year 5m candles with continuous timestamps and source SHA before attempting any missing 20m strategy run. Mark unsupported market/timeframe unavailable rather than fabricating bars.
4. Rebuild all-family and strict Kelly Top100 rankings only from verified nine-market records; keep raw trade provenance and unverified flags.

No Jules, no new workflow, no main change. This report is a diagnostic artifact, not evidence of completed new backtests.
