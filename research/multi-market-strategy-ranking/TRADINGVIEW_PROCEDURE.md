# TradingView Strategy Tester Run Procedure

This document outlines the procedure for compiling and running the Pine Script v6 strategies in the TradingView Strategy Tester to obtain verifiable backtest evidence. All scripts are currently marked as `未測` (Untested) and `UNVERIFIED` because they have not been run on the TradingView platform.

## Prerequisites

1.  A TradingView account (Pro/Premium recommended for deep historical data, especially for lower timeframes if applicable, though all current strategies are 1D).
2.  Access to the TradingView chart for the target symbol (e.g., `BINANCE:BTCUSDT.P` for Crypto futures, `CME_MINI:ES1!` for traditional futures).

## Execution Procedure

For each of the 30 Pine scripts located in the `pine/` directory:

1.  **Open TradingView Pine Editor:** Open a chart, click on "Pine Editor" at the bottom.
2.  **Paste Code:** Open the corresponding `.pine` file from the repository, copy its entire contents, and paste it into the Pine Editor, replacing any existing code.
3.  **Compile & Add to Chart:** Click "Add to Chart" or "Update on Chart". This triggers the TradingView Pine Script v6 compiler.
    *   **Note:** If compilation errors occur, they must be recorded in the Evidence Matrix, and the script requires fixing. The current status in this repo does *not* claim successful compilation without this step.
4.  **Configure Symbol and Timeframe:**
    *   Set the chart symbol to match the target market in the strategy's documentation (e.g., `BINANCE:DOGEUSDT` for Crypto, `OANDA:EURUSD` for Forex, `COMEX:GC1!` for Gold futures).
    *   Set the chart timeframe to 1D (Daily).
5.  **Configure Strategy Properties:**
    *   Open the Strategy Tester tab.
    *   Click the gear icon (Settings) on the loaded strategy.
    *   Ensure the "Properties" tab matches the `initial_capital`, `default_qty_type` (percent of equity), `default_qty_value` (position sizing percentage from the Python Kelly/Fixed-risk results), `commission`, and `slippage` (ticks) as defined in the Python script or Pine script header comments.
6.  **Run Backtest & Export:**
    *   TradingView will automatically calculate the backtest.
    *   Navigate to the "List of Trades" tab in the Strategy Tester.
    *   Export the trade log to CSV.
7.  **Parity Verification:**
    *   Compare the TradingView trade log (entry/exit dates, prices, profit/loss) against the Python-generated trade log for the exact same period and asset.
    *   Calculate the correlation or matching percentage of trades.

## UNVERIFIED Evidence Matrix

Until the above procedure is executed manually by a user on the TradingView platform, the following evidence remains **UNVERIFIED**:

1.  **Compilation Status:** Whether the v6 script compiles without syntax or runtime errors on TV.
2.  **Trade Matching Rate:** The exact percentage of trades matching the Python backtest.
3.  **Slippage/Commission Parity:** Whether the TV slippage (ticks) and commission models perfectly align with the Python approximations.
4.  **OOS Performance:** Real out-of-sample forward test performance on TV.

*Do not merge or claim final product completion until this manual verification is complete for all 30 scripts.*

### Evidence Matrix (To be filled by User)

| Script Name | Compilation (Pass/Fail) | Total Trades (Python) | Total Trades (TV) | Trade Match Rate (%) | Out-Of-Sample Net Profit (TV) | Final TV Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `bb_reentry_rsi_adx25.pine` | [ ] | | | | | UNVERIFIED |
| `bollinger20_2.pine` | [ ] | | | | | UNVERIFIED |
| `bollinger20_rsi14_reentry.pine` | [ ] | | | | | UNVERIFIED |
| `donchian20_10.pine` | [ ] | | | | | UNVERIFIED |
| `donchian20_adx14.pine` | [ ] | | | | | UNVERIFIED |
| `donchian20_macd.pine` | [ ] | | | | | UNVERIFIED |
| `donchian20_volume_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `ema200_macd_cross.pine` | [ ] | | | | | UNVERIFIED |
| `ema200_rsi14_pullback.pine` | [ ] | | | | | UNVERIFIED |
| `ema200_rsi2_extreme.pine` | [ ] | | | | | UNVERIFIED |
| `ema20_50_adx20.pine` | [ ] | | | | | UNVERIFIED |
| `ema50_200.pine` | [ ] | | | | | UNVERIFIED |
| `keltner20_15atr_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `macd12_26_9.pine` | [ ] | | | | | UNVERIFIED |
| `macd_ema200_adx20.pine` | [ ] | | | | | UNVERIFIED |
| `macd_rsi50.pine` | [ ] | | | | | UNVERIFIED |
| `rsi14_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `rsi2_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `stoch14_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `supertrend10_3.pine` | [ ] | | | | | UNVERIFIED |
| `supertrend_adx20.pine` | [ ] | | | | | UNVERIFIED |
| `supertrend_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `supertrend_ema200_flip.pine` | [ ] | | | | | UNVERIFIED |
| `supertrend_rsi50.pine` | [ ] | | | | | UNVERIFIED |
| `turtle55_20_ema200.pine` | [ ] | | | | | UNVERIFIED |
| `volume_donchian20.pine` | [ ] | | | | | UNVERIFIED |
| `wema20_50_daily_donchian20.pine` | [ ] | | | | | UNVERIFIED |
| `wema20_50_daily_macd.pine` | [ ] | | | | | UNVERIFIED |
| `wema20_50_donchian20.pine` | [ ] | | | | | UNVERIFIED |
| `wema20_50_macd.pine` | [ ] | | | | | UNVERIFIED |
