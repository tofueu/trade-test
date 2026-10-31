# 2026-10-31 22:07（台灣）五年增量去重及 SHA256 驗證

本輪在 ChatGPT Python 容器實際執行 `/mnt/data/trade_test_run6_verify.py`，掃描本地 `/mnt/data/*.zip` 65 份，讀取直接 ZIP 或內嵌 TAR.GZ 的 `manifest.json`、`ranking.csv`、`trades.csv`。依 `(symbol,timeframe,family)` 去重；只接受 `status=complete`、`start_utc=2021-10-10`、`end_exclusive_utc=2026-10-10`，且兩份 CSV 的實際 SHA256 均吻合 manifest。

- 解析 153 份完整結構工件；去重後 **138 批**；**138/138** 通過 complete + 五年窗口 + 雙 SHA256；**0 不一致、0 解析錯誤**。
- 分市場去重數：BTCUSDT 38、ETHUSDT 48、SOLUSDT 36、GC=F 4、SI=F 4、ES=F 4、NQ=F 4；本地目前未持有 ^TWII、USDJPY=X 可驗的五年 complete + 雙 SHA 工件。
- 本輪僅確認保存工件完整性；未重新生成 K 線訊號、未逐筆重新驗算所有 Kelly／回撤，也未核對新舊排行是否已包含全部去重批次；不能把 138 與 Git 既有 124 直接相加。**本輪新增從 OHLCV 回測：0**。
- 138 批清單已在執行容器保存為 `/mnt/data/trade_test_run6_local_sha_inventory.csv`，欄位為 symbol/timeframe/family/complete_and_sha/ranking_rows/trade_rows/source；此路徑為對話暫存，不是 Git 上的 CSV。
- 既有舊策略 1d 禁止重跑；其他完整 SHA 工件亦禁止重跑。剩餘範圍依使用者指定 9 市場 × 17 時區、舊31+新7策略；非加密五年分鐘 OHLCV 缺失者 unavailable，禁止合成。20m 僅用四根連續真實5m K線。
- **本輪未更新兩份排行榜數值**，因尚未完成完整 Kelly IS、Bernoulli iid 及 38 策略的去重合併驗證；不可拿未驗算數字覆蓋有效榜單。既有榜單：
  - [五年 Kelly Top100](local_python_kelly_top100_20261030.csv)
  - [全部 38 策略家族](local_python_38_families_20261030.csv)
- 本輪可核實的阻礙：本地已保存工件不覆蓋所有 9 市場/17 時區/策略出場；缺少未完成組合的可靠五年 OHLCV 或可重用完整 artifacts。下輪先收 BTC 1m original+compound、ETH 1m/3m/5m 成功工件並交叉比對已保存的 SHA 與成交回放，再處理真實缺口。
- 不交 Jules、不動 main、不新增 GitHub workflow。專案**未完成**。
