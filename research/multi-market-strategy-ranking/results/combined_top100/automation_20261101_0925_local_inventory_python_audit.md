# Trade Test 2026-11-01 09:25 +08:00 增量稽核

本輪使用 Python 實際讀取先前本地 `trade_test_run6_local_sha_inventory.csv`，對 `(symbol,timeframe,family)` 做唯一鍵檢查、核對指定 9 市場與 17 時區。輸入 CSV SHA256: `3ec2575d8122c58788f4ae248981649683f2ac316dcc813348cb3f805e3d5ebf`。

- 本地庫存 138 列，唯一鍵 138；市場 BTC 38、ETH 48、SOL 36、GC 4、SI 4、ES 4、NQ 4、TWII 0、USDJPY 0；家族 original 36、compound 36、fixed 37、new 29。
- 本地庫存 20m 0 列；僅證明此輸入庫存缺 20m，不證明所有 Git artifacts 均缺。
- Git 上 `signal_backtest_preflight_20261101.json` 另記載 188 筆已存交易回放分類與 424 未驗分類，這與本地 138 列是不同驗證集合，不相加，不以此宣稱原始 OHLCV 訊號已完成。
- 本輪 Python DNS 測試 `data.binance.vision` 和 `raw.githubusercontent.com` 均回傳 `gaierror [Errno -3] Temporary failure in name resolution`；本地容器沒有可直接使用的五年原始 OHLCV。故本輪**新跑出五年原始策略訊號 0 組**、**新驗證 SHA 0 組**、僅舊庫存重新核對 138 列。
- GitHub Actions run 41066783962 的 ETH 1m artifact 12993586056 (151493344 bytes)、ETH 3m artifact 12988929734 (49106611 bytes) 於本輪連接查詢仍顯示未過期；此處僅驗證 metadata，未宣稱 ZIP 內容 SHA 通過。
- 目前不能以 138/612 或 188/612 作為逐策略×市場×時區×出場方法的完整完成率。舊 1d 不重跑；無真實 OHLCV 不補價。
- 下一步：在可讀取 ZIP 內容與真實五年行情的 Python 執行環境，先驗 ETH 1m/3m 工件內層 manifest/ranking/trades SHA，建立逐策略出場唯一鍵；再從連續真實 5m OHLCV 產生 20m 並執行未完成策略，保存逐筆交易、K線 SHA、manifest。保留現有兩榜，不以舊成交回放冒充新訊號回測。

未交 Jules、未新增 workflows、未動 main。