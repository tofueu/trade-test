# 舊＋新策略，全部策略家族排名

這份榜單涵蓋所有研究來源策略家族：舊31種、新7種（名稱可能重疊），不因交易不足70筆或五年收益不足100%而消失。故為38列，**不得補造100種**。

每一來源×策略取現有配置的最高五年收益；『此家族至少有一個合格配置』是檢查家族內其他配置是否有符合交易、收益、回撤與Kelly數值限制。

Kelly倉位數值合格不代表伯努利獨立同分布已證實；原始交易序列未隨CSV提供。

| 策略家族名次 | 來源 | 策略 | 商品 | 週期 | 倉位法 | 五年收益_pct | 五年交易數 | IS_Kelly_pct | 實際風險_pct | Kelly倉位數值合格 | 此家族至少有一個合格配置 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 舊（日線多市場） | MACD12_26_9 | XRPUSDT | 1d | 全凱利 | 1480.77% | 122 | 20.07% | 20.07% | True | True |
| 2 | 舊（日線多市場） | Supertrend+RSI50 | SOLUSDT | 1d | 全凱利 | 1217.89% | 117 | 20.08% | 20.08% | True | True |
| 3 | 舊（日線多市場） | Supertrend10_3 | SOLUSDT | 1d | 全凱利 | 1028.20% | 39 | 24.54% | 24.54% | True | False |
| 4 | 舊（日線多市場） | Supertrend+EMA200 | SOLUSDT | 1d | 全凱利 | 1018.14% | 44 | 23.54% | 23.54% | True | False |
| 5 | 舊（日線多市場） | Stoch14+EMA200 | GC=F | 1d | 全凱利 | 994.66% | 35 | 39.92% | 39.92% | True | False |
| 6 | 舊（日線多市場） | Supertrend+EMA200_flip | NQ=F | 1d | 全凱利 | 807.33% | 16 | 44.43% | 44.43% | True | False |
| 7 | 舊（日線多市場） | WEMA20_50+Donchian20 | NQ=F | 1d | 全凱利 | 757.76% | 18 | 46.03% | 46.03% | True | False |
| 8 | 舊（日線多市場） | WEMA20_50+MACD | SI=F | 1d | 全凱利 | 710.57% | 45 | 26.52% | 26.52% | True | False |
| 9 | 舊（日線多市場） | EMA20_50_ADX20 | DOGEUSDT | 1d | 全凱利 | 680.29% | 13 | 77.36% | 77.36% | True | False |
| 10 | 舊（日線多市場） | Donchian20_10 | SOLUSDT | 1d | 全凱利 | 647.79% | 54 | 39.82% | 39.82% | True | False |
| 11 | 舊（日線多市場） | EMA50_200 | BTCUSDT | 1d | 固定1R | 601.84% | 7 | 0.00% | 10.00% | False | False |
| 12 | 舊（日線多市場） | WEMA20_50+DailyDonchian20 | GC=F | 1d | 全凱利 | 588.37% | 28 | 24.58% | 24.58% | True | True |
| 13 | 舊（日線多市場） | MACD+RSI50 | XRPUSDT | 1d | 全凱利 | 577.02% | 168 | 10.52% | 10.52% | True | True |
| 14 | 舊（日線多市場） | Donchian20_Volume_EMA200 | GC=F | 1d | 全凱利 | 569.57% | 13 | 63.53% | 63.53% | True | False |
| 15 | 舊（日線多市場） | Keltner20_1.5ATR_EMA200 | YM=F | 1d | 全凱利 | 552.47% | 44 | 47.22% | 47.22% | True | False |
| 16 | 舊（日線多市場） | Donchian20+ADX14 | SOLUSDT | 1d | 全凱利 | 485.28% | 65 | 20.28% | 20.28% | True | True |
| 17 | 新（BTC多週期） | Donchian20_Volume_EMA200 | BTCUSDT | 1d | 全凱利 | 471.41% | 29 | 43.19% | 43.19% | True | True |
| 18 | 舊（日線多市場） | EMA200+MACD_cross | GC=F | 1d | 全凱利 | 449.52% | 38 | 20.63% | 20.63% | True | False |
| 19 | 舊（日線多市場） | Donchian20+MACD | DOGEUSDT | 1d | 全凱利 | 434.99% | 60 | 21.56% | 21.56% | True | False |
| 20 | 舊（日線多市場） | Turtle55_20_EMA200 | ETHUSDT | 1d | 全凱利 | 430.22% | 22 | 34.30% | 34.30% | True | False |
| 21 | 舊（日線多市場） | Bollinger20+RSI14_reentry | DOGEUSDT | 1d | 全凱利 | 427.60% | 57 | 17.81% | 17.81% | True | True |
| 22 | 舊（日線多市場） | Supertrend_ADX20 | DOGEUSDT | 1d | 全凱利 | 390.49% | 25 | 40.55% | 40.55% | True | False |
| 23 | 舊（日線多市場） | Volume_Donchian20 | GC=F | 1d | 全凱利 | 377.13% | 15 | 27.68% | 27.68% | True | False |
| 24 | 舊（日線多市場） | EMA200+RSI2_mean_reversion | ES=F | 1d | 全凱利 | 313.68% | 52 | 30.94% | 30.94% | True | False |
| 25 | 舊（日線多市場） | RSI2_EMA200 | ES=F | 1d | 全凱利 | 313.68% | 52 | 30.94% | 30.94% | True | False |
| 26 | 舊（日線多市場） | EMA200+RSI2_extreme | BTCUSDT | 1d | 全凱利 | 276.45% | 51 | 13.54% | 13.54% | True | False |
| 27 | 舊（日線多市場） | EMA200+RSI14_pullback | ETHUSDT | 1d | 全凱利 | 273.39% | 3 | 55.26% | 55.26% | True | False |
| 28 | 舊（日線多市場） | WEMA20_50+DailyMACD | SOLUSDT | 1d | 全凱利 | 268.21% | 36 | 19.66% | 19.66% | True | False |
| 29 | 新（BTC多週期） | Turtle55_20_EMA200 | BTCUSDT | 1d | 全凱利 | 256.96% | 24 | 35.07% | 35.07% | True | True |
| 30 | 舊（日線多市場） | Bollinger20_2 | SI=F | 1d | 全凱利 | 254.68% | 48 | 19.13% | 19.13% | True | True |
| 31 | 新（BTC多週期） | MACD_EMA200_ADX20 | BTCUSDT | 1d | 全凱利 | 220.83% | 42 | 15.09% | 15.09% | True | False |
| 32 | 舊（日線多市場） | MACD_EMA200_ADX20 | BTCUSDT | 1d | 全凱利 | 220.83% | 42 | 15.09% | 15.09% | True | False |
| 33 | 新（BTC多週期） | Keltner20_1.5ATR_EMA200 | BTCUSDT | 12h | 全凱利 | 220.71% | 90 | 10.97% | 10.97% | True | True |
| 34 | 新（BTC多週期） | Supertrend_ADX20 | BTCUSDT | 8h | 全凱利 | 208.47% | 76 | 10.83% | 10.83% | True | True |
| 35 | 新（BTC多週期） | EMA20_50_ADX20 | BTCUSDT | 4h | 全凱利 | 179.88% | 93 | 10.75% | 10.75% | True | True |
| 36 | 舊（日線多市場） | BB_Reentry_RSI_ADX25 | AUDUSD=X | 1d | 半凱利 | 126.21% | 36 | 31.40% | 15.70% | True | False |
| 37 | 新（BTC多週期） | BB_Reentry_RSI_ADX25 | BTCUSDT | 1d | 全凱利 | 72.48% | 31 | 14.06% | 14.06% | True | False |
| 38 | 舊（日線多市場） | RSI14_EMA200 | XRPUSDT | 1d | 全凱利 | 72.44% | 4 | 23.81% | 23.81% | True | False |
