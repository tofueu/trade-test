# Trade Test — 2026-11-01 23:00 +08 — Artifact inventory triage

This run independently queried GitHub Actions Run [41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962) and read the existing 21:20 ETH 1m SHA audit and 21:50 leaderboard uniqueness audit on the isolated report branch.

**New actionable finding:** the first-page inventory contains **31 artifacts**: **14 ZIPs under 1,000 bytes** and **17 ZIPs at least 1,000 bytes**. A ZIP artifact's mere existence is not evidence of a completed five-year signal backtest. Tiny ZIPs require manifest/error payload inspection; they must not be counted complete, and their root cause cannot be inferred from size alone.

Tiny ZIPs (name / bytes / artifact ID):
- SOLUSDT 1m / 293 / 12984099261
- SOLUSDT 3m / 295 / 12985660219
- SOLUSDT 5m / 293 / 12984004347
- SOLUSDT 15m / 296 / 12984258693
- SOLUSDT 30m / 297 / 12984698086
- SOLUSDT 1h / 293 / 12984922402
- SOLUSDT 2h / 293 / 12984632891
- SOLUSDT 4h / 295 / 12983144142
- SOLUSDT 6h / 293 / 12983114375
- SOLUSDT 8h / 294 / 12983029455
- SOLUSDT 12h / 295 / 12983743865
- ^TWII 1d / 287 / 12985281011
- USDJPY=X 1d / 296 / 12984539235
- SOLUSDT 1d / 295 / 12984642354

The 17 larger ZIPs include ETH 1m/3m/5m and other ETH timeframes, several non-crypto daily outputs, and the consolidated ranking artifact. Large size alone also does not certify SHA or source OHLCV.

Existing ETH 1m/3m/5m inner-CSV SHA checks are documented in earlier reports, but independent original OHLCV SHA remains unverified. The prior Top100 is 100 unique saved-ranking keys, **not** 100 newly reproduced signal backtests. Historical 38-family ranking includes 8 out-of-scope market rows.

**This run's counts:** new authentic five-year OHLCV strategy signal configurations = **0**; existing trade replays = **0**; new downloaded ZIP/inner CSV SHA validations = **0**; newly classified artifact inventory records = **31**, of which 14 require failure-payload inspection. No full global completed/required count can be certified without extracting all complete manifests and matching ranking/trade CSVs.

**Next executable repair:** download and inspect a tiny SOL ZIP to determine whether it contains a missing-data/failure marker, then validate Binance authentic daily archives for missing days before any SOL rerun. Collect and SHA-check other already complete artifacts first. For 20m use four consecutive authentic 5m bars, no synthetic gaps. Never rerun legacy 31 × 1d for any of the nine markets. Do not dispatch Jules, create workflows, or touch main.

Historical leaderboards (not fully certified):
- [38-family CSV](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100 CSV](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
