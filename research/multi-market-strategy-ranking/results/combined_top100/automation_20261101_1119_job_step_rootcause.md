# Trade Test 2026-11-01 11:19 +08:00 — GitHub job-step root-cause triage

Source: GitHub REST Actions run 41066783962, 31 jobs and 31 artifacts, independently queried this round.

## Confirmed failure stage
- SOLUSDT 3m job 124100613673: step 6 "Execute four actual strategy families with genuine candles" failed after 66 seconds (2026-10-30 14:22:12Z–14:23:18Z); dependency installation and syntax checks succeeded; artifact preservation/upload succeeded but previously inspected ZIP contained only empty directories. Therefore this is an **execution-stage failure**, not artifact upload failure. Exact exception still requires job log.
- ^TWII 1d job 124100616387: same step 6 failed within ~1 second (14:27:06Z–14:27:07Z). No strategy output; exact exception unverified. **Never rerun legacy 1d**: preserve previously validated daily baseline.
- combine-and-publish job 124178475071: collect, rebuild rankings and upload audited CSV/manifest all **succeeded** (steps 4–6); only step 7 "Commit verified market results to Git without changing main" failed (16:23:14Z–16:23:44Z). Thus **recover the existing verified-multi-market-python-rankings artifact (id 12992239501, 241440493 bytes) before any computation rerun**. Exact push failure still needs log.

## Run-wide inventory
31 jobs: 16 success, 15 failure (12 SOLUSDT, ^TWII 1d, USDJPY=X 1d, combine-and-publish). 31 artifacts; all marked nonexpired as of this query. SOL 12 jobs all failed; ETH 13 succeeded; four futures daily succeeded. Artifact presence is not completion.

## Incremental completion policy
Unique key = market × timeframe × strategy family × strategy × exit. Preserve old 31 strategy daily results for all nine markets without rerunning. First recover BTC 1m original+compound (run 41064675326), ETH 1m/3m/5m and combined published artifact; verify inner manifests, trades and source OHLCV SHA. Do not equate job success or replay with new signals.

## This-round counters
New five-year genuine OHLCV signal backtests: **0**.
New old trade replays: **0**.
New inner CSV or OHLCV SHA checks: **0**.
New verified GitHub job-stage diagnoses: **3**.
Completed/required at per-strategy unique-key granularity: **not computable** until recovered manifest/trades/strategy exit dimensions are joined. Historic 138 category inventory and 124 replay checks are different units; not additive.
20m missing from historic category inventory; genuine contiguous 5m source still required.
No new Kelly Top100 validation. Bernoulli iid unproven.
No Jules, no workflow creation, no main modifications, no reruns.

## Existing leaderboard snapshots (not newly validated)
- [All families](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)
