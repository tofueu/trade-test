# Trade Test 2026-11-01 05:29 +08 — 增量去重與可驗證阻礙

## 本輪實際執行
- GitHub connector 重新查詢 Actions #41064675326 與 #41066783962 的工件中繼資料；BTC original 1m (artifact 12990135479, 112080486 bytes)、compound 1m (12989801317, 16555494 bytes)、ETH 1m (12993586056, 151493344 bytes)、ETH 3m (12988929734, 49106611 bytes)、ETH 5m (12986299665, 28902635 bytes) 均顯示 expired=false。工件存在**不代表本輪下載內容並通過 SHA**。
- Python pandas 實際讀取前輪保存在本地的 `trade_test_run6_local_sha_inventory.csv`，共 138 筆，欄位 symbol/timeframe/family/complete_and_sha/ranking_rows/trade_rows/source。按 symbol 聚合：BTC 38、ETH 48、SOL 36、GC 4、SI 4、ES 4、NQ 4；^TWII 與 USDJPY 為 0。此清單是前輪保存工件的快照，不能當作全 Git 完成集合。
- **查出明確的去重清單缺漏**：前輪本地 138 筆快照對 BTCUSDT 1m 僅有 fixed 一筆，沒有 original 與 compound；但 GitHub 仍保存兩份工件，且先前報告曾驗其排名/交易 CSV SHA。因此下一輪必須以 `(market,timeframe,family,strategy,exit)` 跨工件合併，不能以 138 批當完整完成數，也不能因快照漏列就重跑。
- 讀取兩份既有排行 CSV 的表頭與前幾筆；38 家族榜第 3 名是 XRPUSDT 1d，欄位「本次指定市場」為 False，表示該榜仍含歷史非指定市場資料。後續產出本次任務的榜單須依 9 指定市場篩選；保留原始歷史榜作為可追溯基準，不直接覆蓋。

## 本輪驗收狀態
- 本輪新從五年真實 OHLCV 計算策略入出場：**0 個配置**。
- 本輪新通過交易/排名 CSV SHA：**0 批**（只核對既有快照與 GitHub metadata）。
- 本輪新完成成交回放：**0 批**。
- 完整逐策略 required/completed 尚未重建，故不得使用 124/612 或 138 作為逐策略完成率；38 策略 × 9 市場 × 17 時區僅為未扣 unavailable/出場法的理論格數。
- 原始 K 線 SHA、五年新訊號計算、IS Kelly/伯努利 iid 尚未新增證據；兩份榜單保持原樣。

## 可執行修復順序
1. 先取得 BTC 1m original/compound 與 ETH 1m/3m/5m 的 ZIP 內容，逐 family 驗 manifest complete、五年起訖、ranking/trades SHA256，合併先前已驗紀錄；成功批次絕不重跑。
2. 取得既有 Python 策略實作及五年真實 OHLCV，從尚未完成配置優先 20m (4 根無缺口真實 5m) 進行新策略訊號計算；行情缺失則 unavailable。
3. 從完整成交證據產生 9 市場限定的全部 38 家族榜及 >=70 筆、>100% 收益、實際風險 <= IS Kelly 的去重 Top100；伯努利 iid 未證明不得宣稱通過。

原榜：[38 家族](local_python_38_families_20261030.csv)；[Kelly Top100](local_python_kelly_top100_20261030.csv)。

未動 main、未新增 workflow、未交 Jules。此次是驗收清單缺漏定位與可追溯 Git 工件查核，**不是**新策略回測完成。
