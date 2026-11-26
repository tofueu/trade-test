# 跟隨圖表商品與週期：26份 Pine 修正草稿

範圍：第2、5、8～31名。第1、3、4、6、7名未修改。每種策略各一份可獨立載入的Pine。

**狀態：已完成原Python訊號規則對照；TradingView編譯、成交與績效尚未實測，不能標示排名重現或自動交易驗證通過。**

## 跟隨方式

- OHLCV與進出場指標使用圖表商品、K棒週期。切SOL／BTC或3H／1H／15M不必另寫相同邏輯。
- EMA20表示20根目前圖表K棒，Donchian20表示前20根圖表K棒；策略名稱中的Daily沿用原名稱，不代表鎖死日線。
- 第12、18、20、28名原本有週線方向過濾，因此保留前一完整週線，進場訊號仍用當前圖表週期；不同交易所週線／交易時段需另外核對。
- 圖表右上角顯示當前商品與週期；相關價格指標會繪圖，訊號狀態／週線方向可在資料視窗檢查。
- 不自動選最佳參數，也不在切圖表後重新計算Kelly。風險、ATR止損、固定TP與移動止損可調；預設值是原排名參考配置。
- 第22名沒有找到完全對應的原排名列，保留舊Pine的可調預設值並標示未確認，沒有猜造新Kelly或出場參數。
- 無交易截止日。保留參考暖機與交易開始時間；載入歷史不足會顯示提示。比較排名須使用相同起訖區間、資料來源、商品、週期與成本。

## 選擇代碼

|名次|策略|參考商品／週期（不是鎖定）|風險%預設|固定TP R|移動ATR|參數來源|
|---:|---|---|---:|---:|---:|---|
|2|[Volume_Donchian20](pine/Volume_Donchian20.pine)|BTCUSDT / 8h|20.276138|0|0|保存的原排名列|
|5|[Donchian20_10](pine/Donchian20_10.pine)|SOLUSDT / 6h|17.472234|0|0|保存的原排名列|
|8|[Donchian20_Volume_EMA200](pine/Donchian20_Volume_EMA200.pine)|SOLUSDT / 3h|15.773755|3|0|保存的原排名列|
|9|[EMA20_50_ADX20](pine/EMA20_50_ADX20.pine)|SOLUSDT / 4h|26.206081|3|0|保存的原排名列|
|10|[Donchian20+MACD](pine/Donchian20_MACD.pine)|SOLUSDT / 8h|17.380075|4|0|保存的原排名列|
|11|[Keltner20_1.5ATR_EMA200](pine/Keltner20_1_5ATR_EMA200.pine)|SOLUSDT / 3h|14.752074|2|0|保存的原排名列|
|12|[WEMA20_50+MACD](pine/WEMA20_50_MACD.pine)|BTCUSDT / 12h|20.214340|0|0|保存的原排名列|
|13|[MACD+RSI50](pine/MACD_RSI50.pine)|SOLUSDT / 3h|10.000000|0|0|保存的原排名列|
|14|[Turtle55_20_EMA200](pine/Turtle55_20_EMA200.pine)|SOLUSDT / 6h|19.670926|3|0|保存的原排名列|
|15|[Supertrend+EMA200_flip](pine/Supertrend_EMA200_flip.pine)|SOLUSDT / 6h|19.852709|2|0|保存的原排名列|
|16|[MACD_EMA200_ADX20](pine/MACD_EMA200_ADX20.pine)|SOLUSDT / 12h|18.946524|3|0|保存的原排名列|
|17|[Donchian20+ADX14](pine/Donchian20_ADX14.pine)|BTCUSDT / 6h|10.000000|3|0|保存的原排名列|
|18|[WEMA20_50+Donchian20](pine/WEMA20_50_Donchian20.pine)|SOLUSDT / 6h|16.717818|4|0|保存的原排名列|
|19|[EMA200+MACD_cross](pine/EMA200_MACD_cross.pine)|SOLUSDT / 12h|27.599418|0.5|0|保存的原排名列|
|20|[WEMA20_50+DailyDonchian20](pine/WEMA20_50_DailyDonchian20.pine)|SOLUSDT / 8h|17.027453|1|0|保存的原排名列|
|21|[Supertrend_ADX20](pine/Supertrend_ADX20.pine)|ETHUSDT / 6h|10.000000|3|0|保存的原排名列|
|22|[Bollinger20+RSI14_reentry](pine/Bollinger20_RSI14_reentry.pine)|USDJPY=X / 1d|17.806000|3|0|**舊版保留，排名未確認**|
|23|[Bollinger20_2](pine/Bollinger20_2.pine)|BTCUSDT / 1d|18.425952|4|0|保存的原排名列|
|24|[EMA200+RSI14_pullback](pine/EMA200_RSI14_pullback.pine)|SOLUSDT / 30m|10.963384|2|0|保存的原排名列|
|25|[RSI14_EMA200](pine/RSI14_EMA200.pine)|SOLUSDT / 30m|11.885849|0|3|保存的原排名列|
|26|[EMA200+RSI2_mean_reversion](pine/EMA200_RSI2_mean_reversion.pine)|ETHUSDT / 8h|12.259303|1|0|保存的原排名列|
|27|[RSI2_EMA200](pine/RSI2_EMA200.pine)|ETHUSDT / 8h|12.259303|1|0|保存的原排名列|
|28|[WEMA20_50+DailyMACD](pine/WEMA20_50_DailyMACD.pine)|SOLUSDT / 12h|10.000000|3|0|保存的原排名列|
|29|[Stoch14+EMA200](pine/Stoch14_EMA200.pine)|ETHUSDT / 8h|10.000000|0.5|0|保存的原排名列|
|30|[EMA200+RSI2_extreme](pine/EMA200_RSI2_extreme.pine)|ETHUSDT / 4h|10.000000|3|0|保存的原排名列|
|31|[BB_Reentry_RSI_ADX25](pine/BB_Reentry_RSI_ADX25.pine)|BTCUSDT / 6h|10.000000|3|0|保存的原排名列|

## 修正內容

依原Python重寫EMA／ATR／RSI／ADX的EWM初始化、自訂Supertrend與狀態條件；全域計算歷史狀態，避免短路條件中的歷史函式；僅收盤時計算並於下一根開盤成交；進場時提交初始止損／止盈；反轉不重複送平倉單。
固定RR策略保持事件進場及固定出場；訊號持倉策略保持原狀態轉換；第9、13名依Python真實程式的ADX出場／MACD等號邊界修正。

## 已驗證與未驗證

- 使用既有真實SOLUSDT 3H快取行情，26種規則翻譯後的訊號狀態逐根比對原Python函式，全部一致；這是規則測試，不是26種商品／週期完整績效回測。
- RSI／ATR／ADX與週線EMA的逐值遞迴公式比對通過。完整紀錄見[source_checks.json](source_checks.json)。
- Pine編譯、TV broker emulator成交、收益率與筆數±5%：**未測**。固定RR同根K棒出場再進場、同根SL/TP先後、價格百分比滑價及期末平倉可能與Python不同。
- margin_long=0／margin_short=0只對應原Python不模擬名目保證金與強平的研究假設，不能當成交易所槓桿設定。
- 25份已找到的排名配置屬加密合約，預設交易費用0.05%每邊；未模擬Python另有的0.05%價格滑價。換其他市場須在策略屬性核對費率、滑價、合約價值；不會自動下載券商費率。
- 第22名保留舊Pine費率，該費率不是已驗證的USDJPY成本模型。

## TradingView使用

新增一個策略腳本，貼入所選.pine完整內容，再新增到圖表。先單獨測試，不要直接接現有下單Webhook。
切換圖表會改變此腳本的行情計算；已建立的TV快訊是獨立伺服器副本，不會跟著切換。換商品／週期或改程式後須重建快訊，並確認JSON下單商品同步更新。
教材接收端每次固定0.01，不能代表Pine的實際倉位，也不會因本次改碼而自動升級。
本批先放獨立修正分支供TV驗證，沒有覆蓋首頁各排名的現用分支，也沒有修改main或Python原檔。
