# Historical five-year qualification — existing Top 50 only

**Source:** `results/overall_top50.csv` on the existing Trade Test branch. This is a **read-only filter of previously generated daily-bar historical rankings**, not a new strategy search, new five-year run, intraday backtest, or TradingView/Python parity validation.

- Historical window stated in the research README: 2021-10-10 through 2026-10-10 UTC (daily bars).
- Acceptance gates: five-year return **strictly >100%**, closed trades **>=70**, IS Kelly **>0**. Returns are research estimates with stated trading-cost assumptions.
- **9 of 50 rows** in the historical Top 50 pass these three gates; repeated strategy/market pairs with different exit or sizing settings are **not independent strategies**.
- This file does **not** claim the full 9,556-row gzip archive has been scanned. To filter the complete archive without overwriting it, run:
  `python src/filter_qualified_five_year.py --input results/complete_ranking_9556.csv.gz --output results/qualified_five_year_gt100_70trades.csv`
- Positive Kelly is an in-sample estimate, not a guarantee. High drawdown and overfitting remain risks. The user requested multi-timeframe and new-strategy testing; that remains separate unfinished work.

| Original rank | Strategy | Market | Five-year return | Trades | IS Kelly | Max drawdown | OOS return |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | MACD12_26_9 | XRPUSDT | 1480.77% | 122 | 20.07% | 49.60% | 77.78% |
| 2 | Supertrend+RSI50 | SOLUSDT | 1217.89% | 117 | 20.08% | 28.93% | 183.08% |
| 10 | MACD12_26_9 | XRPUSDT | 740.38% | 122 | 20.07% | 25.97% | 38.89% |
| 11 | MACD12_26_9 | XRPUSDT | 737.91% | 122 | 20.07% | 25.93% | 38.76% |
| 18 | Supertrend+RSI50 | SOLUSDT | 608.95% | 117 | 20.08% | 20.69% | 91.54% |
| 19 | Supertrend+RSI50 | SOLUSDT | 606.59% | 117 | 20.08% | 20.64% | 91.18% |
| 25 | MACD+RSI50 | XRPUSDT | 577.02% | 168 | 10.52% | 85.95% | 49.40% |
| 33 | MACD+RSI50 | XRPUSDT | 548.57% | 168 | 10.52% | 83.48% | 46.97% |
| 47 | MACD12_26_9 | Silver | 475.26% | 104 | 17.27% | 42.84% | 57.15% |
