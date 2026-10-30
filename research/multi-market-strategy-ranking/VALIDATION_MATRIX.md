# Pine Script Validation Matrix

This matrix validates the equivalence of Python backtests and TradingView Pine scripts.
It strictly requires offline parity vs real TradingView run evidence (`tv_evidence`).
If real TradingView credentials/interactions are needed but absent, scripts remain UNVERIFIED.

| Script Name                       | Compilation           | Run Status        | Parity (Strict)   | Overall Status   | Notes       |
|:----------------------------------|:----------------------|:------------------|:------------------|:-----------------|:------------|
| `bb_reentry_rsi_adx25.pine`       | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `bollinger20_2.pine`              | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `bollinger20_rsi14_reentry.pine`  | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `donchian20_10.pine`              | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `donchian20_adx14.pine`           | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `donchian20_macd.pine`            | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `donchian20_volume_ema200.pine`   | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema200_macd_cross.pine`          | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema200_rsi14_pullback.pine`      | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema200_rsi2_extreme.pine`        | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema20_50_adx20.pine`             | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema50_200.pine`                  | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `ema_cross_5m_pending.pine`       | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `keltner20_15atr_ema200.pine`     | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `macd12_26_9.pine`                | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `macd_adx20_tp15.pine`            | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `macd_ema200_adx20.pine`          | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `macd_rsi50.pine`                 | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `macd_rsi50_tp15.pine`            | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `rsi14_ema200.pine`               | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `rsi2_ema200.pine`                | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `rsi_15m_pending.pine`            | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `stoch14_ema200.pine`             | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `supertrend10_3.pine`             | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `supertrend_adx20.pine`           | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `supertrend_ema200.pine`          | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `supertrend_ema200_flip.pine`     | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `supertrend_rsi50.pine`           | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `turtle55_20_ema200.pine`         | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `volume_donchian20.pine`          | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `wema20_50_daily_donchian20.pine` | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `wema20_50_daily_macd.pine`       | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `wema20_50_donchian20.pine`       | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |
| `wema20_50_macd.pine`             | TV_COMPILE_UNVERIFIED | TV_RUN_UNVERIFIED | N/A               | UNVERIFIED       | No evidence |