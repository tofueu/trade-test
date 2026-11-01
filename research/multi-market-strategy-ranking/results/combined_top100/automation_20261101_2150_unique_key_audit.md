# Trade Test — 2026-11-01 21:50 +08 — Incremental leaderboard uniqueness audit

This run fetched two full CSVs from the existing report branch and recomputed their in-scope and unique-key counts. This is a **saved-ranking audit only**, not a new five-year OHLCV signal backtest and not an independent source-OHLCV hash check.

- 38-family historical ranking rows: 38; in nine specified markets and 17 timeframes: 30; excluded as out of scope: 8.
- Historical Top100 rows: 100; unique market×timeframe×family×strategy×exit keys: 100; duplicates within this leaderboard: 0.
- Rows meeting numerical trade>=70, return>100%, risk<=IS Kelly with 1e-8 floating tolerance: 100. This **does not certify** independently reproduced strategy signals or Bernoulli iid.
- Top100 source statuses: {"trade_fills_replayed_locally_sha256":98,"complete_sha256_verified":2}.
- Timeframe distribution: {"8h":34,"2h":4,"6h":22,"12h":23,"4h":15,"1d":2}.
- CSV integrity/manifest verification newly performed this run: **0**. New OHLCV signal combinations: **0**; trade replays: **0**. Verified completed/required global configurations: **not established**, because full manifest-to-ranking provenance and independently verified market OHLCV are still missing.

## Incremental next action

Collect all status=complete manifest/CSV artifact inventories and their SHA checks, construct global unique-key ledger with independent status columns for artifact presence, CSV SHA, replay and original-OHLCV verification. Never rerun any of the 31 legacy families at 1d for any of the nine markets; only run missing combinations on authentic complete five-year OHLCV. 20m must use four contiguous authentic 5m bars, never synthetic gap fills. Do not use Jules, create workflows or modify main.

- [38-family historical CSV](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100 historical CSV](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
