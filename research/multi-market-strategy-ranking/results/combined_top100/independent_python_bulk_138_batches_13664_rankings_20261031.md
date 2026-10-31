# Trade Test 2026-10-31 本地 Python 增量回放：138 批、13,664 配置

本輪在 Python 執行 `/mnt/data/trade_test_bulk_replay.py`，完整讀取本地保存的 GitHub Actions 原始 ZIP / tar.gz 工件並比對 `manifest.json` 內兩個 SHA256。只處理具有 `2021-10-10` 至 `2026-10-10` exclusive 的真實五年交易工件，按 (symbol,timeframe,family) 去重。

**最後結果：138 個不同分類批次、13,664 筆排名配置，13,664 筆全部可用各配置的實際風險%及前 N 筆真實 R 獨立重建五年收益，誤差門檻 1e-6 百分點；0 筆不一致、0 份 ZIP/manifest 解析錯誤。** 計算式 `max(-100, risk_pct * sum(trade_R[:five_year_trade_count]))`，原始策略採固定初始資金風險、非複利。

在前輪累計 101 批 / 10,180 配置之後，這次另從成功的 GitHub Actions #41068912974 下載 10 件工件，包含 SOLUSDT 的 6h、8h、4h、2h、1h、30m、1d，ETHUSDT 45m/10m，以及 BTCUSDT 2m；全部再次跑 Python 去重回放，**淨增 37 個不重複批次、3,484 筆可重建收益排名配置**。GitHub 工件 IDs：`12995845267,12994593468,12994453394,12993804891,12995876406,12995093638,12995175266,13008084264,13008442746,13009908276`。

本輪本地完整批次 CSV 檔：`/mnt/data/TradeTest_bulk_independent_return_replay_20261031.csv`（138 行，當前會話可下載，**未將 CSV 檔本身提交此 Git 分支**）。

**驗證限制：** 成果屬於已保存工件的原始逐筆交易 R 與五年淨收益獨立回放，不代表從原 OHLCV 重生成策略訊號；Kelly 與 drawdown 尚未全面獨立核對。與既有 Git 124 個已驗批次有重疊，**不得直接將 138 加 124**；此次只是本地已重新核實的分類集合擴大。完整 9 市場、17 時區、舊31+新7策略仍有待補完。未交 Jules、未改 main、未新增 workflow。
