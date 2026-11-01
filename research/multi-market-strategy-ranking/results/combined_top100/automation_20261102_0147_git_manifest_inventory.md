# 2026-11-02 01:47 +08:00 — Git manifest 去重範圍盤點

本輪重新讀取隔離分支完整 Git tree（truncated=false），不是沿用排行榜推估。

## 可核實的新結果
- Git tree 中共有 **30 份** `results/all_timeframes/**/manifest.json`，涵蓋 **8 個 market×timeframe**：BTCUSDT 1d/4h（各3家族）；ETHUSDT 1d/4h（各4家族）；GC=F、SI=F、ES=F、NQ=F 的 1d（各4家族）。
- 這只是 **Git 分支內 manifest 存在數**，不包含尚未回收至 Git 的 Actions artifacts；絕不可作為已完成策略配置數。
- Git tree 沒有 SOLUSDT、^TWII、USDJPY=X 的 manifest；不代表其他 artifacts 或舊測試不存在。
- 實際讀取 ETHUSDT 1d new manifest：status=complete、strategy_count=7、bar_count=1826、missing_or_irregular_intervals=0、ohlcv_sha256=1bda04871f1d547da535bcca9d73ab4e3d4ad3bbfb39dc1edf2bbd84e67b4e44、ranking_sha256=96740666c4c07f7b86ec43852fa995ca6feda51fcdb17048a484094b8b2ea595、trades_sha256=f383ce34a8bf27c4509ae9fb59e41b47a886b173a52a5ecbb8829367bc849071。這些是**manifest 宣告值**，尚未獨立重算原始 OHLCV SHA。
- 此 new manifest 7 策略各 tested_exit_count=5，但 saved_exit_count=1；不能把未保存的出場配置列為已驗收。
- 讀取失敗 job 日誌 API `/actions/jobs/{id}/logs` 時，連接器回傳「URL 不允許」，本輪沒有取得 stderr；因此 SOL 根因仍不能斷定。

## 本輪完成口徑
- 新跑出五年 OHLCV 策略訊號：**0 組**。
- 舊交易紀錄回放：**0 組**。
- 新增 SHA 獨立驗證：**0 份**。
- Git manifest 存在性盤點：**30 份／8 個市場週期群組**；完整 verified completed/required **未知**。
- 38 家族榜與 Kelly Top100 未修改，伯努利 iid 未證明。
- 所有九市場舊策略 1d **禁止重跑**；其餘配置按 market×timeframe×family×strategy×exit 去重後補缺。

## 下一輪具體動作
先回收 Actions 工件 manifest 並建立全域唯一鍵；取得失敗 job 的 stderr（現有連接器阻擋 logs URL，可改由授權的檔案下載或現有 workflow 日誌取得），查明 SOL 空工件根因。驗證真實五年連續 OHLCV 後，只補缺失非 1d 配置；20m 必須由四根真實連續 5m 合成。

既有排行榜：
- [38 家族榜](./local_python_38_families_20261030.csv)
- [Kelly Top100](./local_python_kelly_top100_20261030.csv)

原始 Run：https://github.com/tofueu/trade-test/actions/runs/41066783962
