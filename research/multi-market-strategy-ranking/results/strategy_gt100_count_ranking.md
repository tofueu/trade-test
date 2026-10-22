# 策略名稱「五年收益 > 100%」次數排名

- 來源：`results/complete_ranking_9556.csv.gz`（完整五年多市場總榜）
- 母體：9,556 個排名配置列；共 31 個不同的「策略」名稱。
- 篩選：嚴格大於 100（`五年收益_pct > 100`）；等於 100 不計。
- 統計：符合條件的配置列共 904 列；同一策略在不同商品、出場方式及倉位配置會各自計為一列。這是「配置列命中次數」，不是去重後的獨立交易數，也不是策略邏輯數。
- 排序：命中列數由高至低；收益欄位沿用原總榜的五年累積收益_pct（2021-10-10 至 2026-10-10，UTC），不是 OOS 欄位。OOS 收益 >100% 的 67 列不參與本排名。
- 30 個有命中的名稱如下；另有 1 個策略名稱在完整資料中沒有任何列超過 100%。

| 排名 | 策略名稱 | 五年收益 >100% 的配置列數 |
|---:|---|---:|
| 1 | MACD12_26_9 | 130 |
| 2 | Donchian20_10 | 110 |
| 3 | Supertrend10_3 | 100 |
| 4 | EMA50_200 | 44 |
| 5 | Volume_Donchian20 | 41 |
| 6 | MACD+RSI50 | 39 |
| 7 | RSI2_EMA200 | 36 |
| 8 | Supertrend+RSI50 | 35 |
| 9 | Donchian20+MACD | 31 |
| 10 | Supertrend+EMA200 | 29 |
| 11 | Supertrend+EMA200_flip | 27 |
| 12 | WEMA20_50+MACD | 25 |
| 13 | WEMA20_50+DailyDonchian20 | 24 |
| 14 | Bollinger20_2 | 23 |
| 15 | Bollinger20+RSI14_reentry | 21 |
| 16 | Donchian20+ADX14 | 21 |
| 17 | WEMA20_50+Donchian20 | 19 |
| 18 | EMA200+MACD_cross | 18 |
| 19 | Keltner20_1.5ATR_EMA200 | 18 |
| 20 | WEMA20_50+DailyMACD | 18 |
| 21 | EMA200+RSI2_extreme | 16 |
| 22 | Donchian20_Volume_EMA200 | 14 |
| 23 | EMA20_50_ADX20 | 14 |
| 24 | Supertrend_ADX20 | 13 |
| 25 | Turtle55_20_EMA200 | 12 |
| 26 | Stoch14+EMA200 | 9 |
| 27 | EMA200+RSI2_mean_reversion | 7 |
| 28 | MACD_EMA200_ADX20 | 5 |
| 29 | BB_Reentry_RSI_ADX25 | 3 |
| 30 | EMA200+RSI14_pullback | 2 |

## 解讀限制

這個排名衡量各策略名稱在總榜不同配置中「五年收益超過 100%」的出現頻率，不等同於平均收益、風險調整績效或獨立商品數。完整排名會包含同一商品/策略在不同出場方式與倉位法下的多列，因此配置設計較多的策略可能有較多命中機會。
