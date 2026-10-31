# Trade Test 2026-11-01 06:21 +08 — 排名範圍修正與驗收界線

本輪使用 GitHub connector 實際讀取既有兩份排行榜及前輪 05:29 稽核報告。既有 38 家族榜共有 38 列，其中指定九市場 30 列；其餘 8 列屬非指定市場，不能納入本次驗收。已產出不覆蓋舊榜的九市場限定 CSV 快照。

本輪新從五年真實 OHLCV 計算策略訊號：**0 組**。本輪新驗證交易 CSV SHA：**0 批**。本輪新增已驗成交回放：**0 批**。原因：本輪連接器可讀 Git 文字檔，但未取得可在 Python 環境中使用的五年 OHLCV 和完整策略程式；不能以舊榜篩選冒充新策略訊號回測。未聲稱完成逐策略 required/completed。

BTC 1m original/compound 與 ETH 1m/3m/5m 工件需繼續逐一驗 ZIP/TAR、manifest、排名及交易 SHA；工件存在不能等同驗證。下一步優先取得真實 5m OHLCV 及 20m 策略實作，先排除已完整原始回測配置，再以四根連續真實 5m K 線產生新訊號。舊策略 1d 禁止重測。非加密分鐘行情缺五年真實資料標 unavailable，不造價。IS Kelly/伯努利 iid 未有新增驗證。

原始榜：[38 家族](local_python_38_families_20261030.csv)、[Kelly Top100](local_python_kelly_top100_20261030.csv)。九市場篩選榜：[CSV](automation_20261101_0621_nine_market_family_snapshot.csv)，屬既有歷史排名的範圍修正，**不是完整 38 家族實測新榜**。

未交 Jules、未新增 workflow、未動 main。
