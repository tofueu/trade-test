# 五年 Python 回測工件獨立驗算：188 分類批次／18,592 個排名配置（2026-10-31）

本輪在本對話實際直接執行 Python，優先補上前次因檔案過大超時的 SOLUSDT、ETHUSDT 的 1m/2m 四分類，並再確認 ^TWII 1d 四分類與 BTCUSDT 1m 原始/複合分類。未交 Jules、未轉 Work、未改 main、未增加 workflow。

## 逐筆核對新增結果

- SOLUSDT 1m：original 288、compound 32、fixed 36、new 28，共 **384/384 配置一致**；original 保存約 590 萬筆逐筆 R。
- ETHUSDT 1m：同樣四分類共 **384/384**；original 保存約 606 萬筆逐筆 R。原先超時的 original 以分開執行解決。
- SOLUSDT 2m：四分類 **384/384**。
- ETHUSDT 2m：四分類 **384/384**。
- ^TWII 1d：GitHub artifact `13012196883`，四分類 **384/384**；檢查 manifest 日期，實際日線資料首根 2021-10-12、末根 2026-10-08（休市日不強制要求日 K 連續），bar_count 1213。
- BTCUSDT 1m：GitHub artifact `12989801317` compound **32/32**、artifact `12990135479` original **288/288**，包含 original 約 622 萬筆存檔逐筆 R。

本輪相對前次的 166 分類批次、16,352 配置，**淨增 22 個去重批次及 2,240 筆配置**，截至此次 Python 實際查核為 **188 個互異 (symbol,timeframe,family) 批次、18,592 配置，18,592/18,592 全部五年收益獨立回算吻合，0 個不一致**。SHA256（ranking 和 trades）均符合 manifest；取 `(策略,出場方式)` 前 N 筆真實 R，按 `max(-100, 實際風險_pct * sum(R[:N]))` 與原排名逐列比對、閾值 `1e-6` 個百分點。所有本輪新增工件 manifest 均註明 UTC 五年窗口 2021-10-10 至 2026-10-10 exclusive。

為處理百萬筆逐筆交易，使用分段的 Python 串流 CSV 與 SHA256 計算，避免將整份 ZIP 轉為 DataFrame。原始核查程式在本次對話執行環境：
- `/mnt/data/trade_test_2m_incremental_verify.py`
- `/mnt/data/trade_test_1m_finish_others.py`
- `/mnt/data/eth_1m_debug.py`
- `/mnt/data/trade_test_twii_incremental.py`
- `/mnt/data/trade_test_btc_1m_existing_verify.py`

完整 CSV 明細：`/mnt/data/TradeTest_incremental_BTC1m_merged_20261031.csv`（188 個去重批次、18,592 筆排名配置、0 mismatches，只有本對話暫存檔尚未上傳 Git）。先前 Git 124 批與此處 188 批有重疊，不可相加。

**還沒有全部完成**：本輪執行是已保存實際五年策略逐筆交易紀錄的 SHA256 及收益獨立驗算，**不是從五年 OHLCV 重新跑所有入出場**。目前分類理論範圍仍是 9 市場×17 時區×4 family = 612；本地已驗證 188 批，剩餘 424 批尚未在此會話這種嚴格口徑全部驗收，部分市場日內缺五年真實行情；完整 Kelly、回撤逐列重算與原要求舊31+新7策略碼缺口仍未補齊。不得以 188/612 解讀成 188 種不重複交易策略。不得宣稱全部完成。
