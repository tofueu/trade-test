# Trade Test 2026-11-01 04:31 +08 — ETH 工件增量收取與執行障礙

- 本輪實際查詢 GitHub Actions #41066783962，確認 `market-ETHUSDT-1m` artifact ID `12993586056`，151,493,344 bytes，expired=false；`market-ETHUSDT-3m` artifact ID `12988929734`，49,106,611 bytes，expired=false。
- GitHub Connector 下載兩份工件成功，回傳 `eth_12993586056.zip` 與 `eth_12988929734.zip`；**下載成功不等於 SHA 驗證通過**。
- 嘗試用本地 Python `zipfile` 開啟這兩個 ZIP 並計算 ranking/trades SHA256，但本輪 container 執行呼叫發生 ClientError，Python 核心重設且未完成執行；因此**沒有**本輪 CSV SHA256、K 線 SHA、成交回放或新五年策略訊號結果。下輪應先重試本地執行環境、再對兩份工件逐 family 驗證 manifest status=complete、trades/ranking hash、OHLCV 宣告與歷史時間範圍，並與既有 ETH 5m 四 family 去重。
- 本輪新增 OHLCV 原始訊號回測配置：**0**；本輪新增 SHA 已驗分類批次：**0**；本輪僅成功收取 2 份舊工件。既有 124/612 已驗成交回放、138 個先前 SHA 去重工件是不同口徑，未合併驗收，禁止相加。
- 計畫範圍：舊 31 + 新 7 策略；市場 GC=F, SI=F, BTCUSDT, ETHUSDT, SOLUSDT, ES=F, NQ=F, ^TWII, USDJPY=X；17 時區 1m,2m,3m,5m,10m,15m,20m,30m,45m,1h,2h,3h,4h,6h,8h,12h,1d。已完成舊 1d 禁止重跑；缺五年真實 OHLCV 的市場×時區標 unavailable。market×timeframe×family×strategy×exit 去重 required 尚未重建，不能用 612 當逐策略完成分母。
- Top100 條件：五年、>=70 trades、>100% return、actual risk <= IS Kelly；伯努利 iid 尚未證明。既有排行榜不改動，避免把未驗結果寫入。
- Git 排行：`local_python_38_families_20261030.csv`；`local_python_kelly_top100_20261030.csv`（同 results/combined_top100 目錄）。
- 未動 main、未新增 workflow、未交 Jules；下一輪先修復 Python 容器執行，再做 ETH 1m/3m 的完整 ZIP→TAR→manifest→SHA 查核，優先原始真實行情的缺漏組合。
