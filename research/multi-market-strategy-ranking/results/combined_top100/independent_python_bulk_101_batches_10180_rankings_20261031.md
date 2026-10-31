# 五年 Python 獨立收益回放進展：101 批／10,180 配置（2026-10-31）

## 確實執行
1. 先前讀取本地五年工件 90 批，依每筆實際交易 R 的順序、風險%、截取 N 筆後，固定初始資金加總，以 -100% 截斷。
2. 本輪**另外從 GitHub Actions 41068912974 實際下載** 5 份新工件：`market-BTCUSDT-3h` (artifact 13003955864), `market-BTCUSDT-45m` (13002144342), `market-BTCUSDT-10m` (13002033353), `market-SOLUSDT-3h` (13011284372), `market-SOLUSDT-12h` (12995535103)。
3. 再次完整執行 `/mnt/data/trade_test_bulk_replay.py`，讀取所有當前本地 ZIP/tar.gz；對每一五年完整 manifest、ranking.csv、trades.csv 核對 SHA256；按 `(symbol,timeframe,family)` 去重，不重算重複批次。
4. **累計 101 個不同批次，10,180 筆排名配置全部五年收益逐筆 R 重建吻合，0 個不一致，0 個檔案解析錯誤**，誤差閾值 `1e-6` 百分點。相較前輪 90 批 9,328 配置，**新增 11 個去重批次、852 筆已驗排名配置**（部分工件只有部分 family）。
5. 新工件所有五年期間遵守 `2021-10-10` 至 `2026-10-10` exclusive；均從已保存的真實 GitHub Actions 交易工件驗證，不是造數據。
6. 這是**獨立收益回放驗收，不是重新從 OHLCV 跑交易訊號**，也未涵蓋全部 Kelly/最大回撤重算。此處 101 個本地去重批次和既有 Git 124 個已核實批次有重複，**不可算成 225 批**。以已核實資料為準。
7. 完整 101 行 Python 驗證表已在本次對話執行容器生成：`/mnt/data/TradeTest_bulk_independent_return_replay_20261031.csv`。容器內的原始碼：`/mnt/data/trade_test_bulk_replay.py`。此處路徑不是已提交到 Git 的 CSV。
8. 整體要求仍是 9 市場、17 時區、舊31+新7策略全部五年實測。缺行情／尚未獨立驗證訊號的部分未完成。不得標記全案完成。未交 Jules、未改 main、未新增 workflow。
