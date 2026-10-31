# 五年 Python 獨立收益回放 — 90 批／9,328 配置（2026-10-31）

本輪在 ChatGPT Python 容器實際執行 `/mnt/data/trade_test_bulk_replay.py`，讀取本地保存的 GitHub Actions ZIP / 內嵌 tar.gz 工件，逐份稽核完整五年真實行情來源的 ranking / trades / manifest，並去重。

## 結果

- **90 個不重複 (symbol,timeframe,family) 批次**，**9,328 筆排名配置**。
- 逐批確認 `manifest.start_utc=2021-10-10`、`end_exclusive_utc=2026-10-10`，及 ranking.csv、trades.csv 雙 SHA256 完全吻合。
- 由 `(策略,出場方式)` 分組的實際逐筆 `R`，依原始排名列的 `五年交易數` 與 `實際風險_pct`，用原始固定初始資金倉位模型 `max(-100, risk_pct * sum(R[:N]))` 重算五年收益。
- **9,328 / 9,328 配置的五年收益與原 CSV 完全一致**，誤差門檻 `1e-6` 百分點，**0 不一致**、**0 解析錯誤**。
- 前一步 ETHUSDT 3h 單獨重新取得 artifact ID `13009351170`，含 4 類策略／384 配置／40,459 筆逐筆成交，此次 90 批已包含 ETHUSDT 3h，不可重複計數。
- 本次的 90 個批次是**此執行容器目前持有工件的獨立逐筆回放範圍**，不能直接加到既有全 Git **124 個 SHA + 本機成交重放**已驗證批次，因為兩個集合存在重疊，而且既有 Git 集合可能較大。
- 此次獨立驗證的是**五年收益及每列 trade 計數可重建**，並非從原始 OHLCV 重跑 90 次策略訊號，也**沒有獨立驗算所有排名列的 Kelly 推估與最大回撤**，不要擴大驗證宣稱。
- 此時仍未完成全部 9 市場×17 時區×4 分類共 612 分類批次，也未補齊原定 31 舊 + 7 新策略碼缺口。缺少可靠五年 OHLCV 的市場時區仍標記 unavailable，不得編造。
- 本輪實際生成的逐批查核清單：`/mnt/data/TradeTest_bulk_independent_return_replay_20261031.csv`，共 90 列，顯示 symbol,timeframe,family,ranking_rows,exact_return_matches,mismatches,source。Python 驗證腳本同會話目錄內，該暫存路徑**不是 Git 上已有檔案**。
- 保留 `main` 不變，不交 Jules，不新增 Actions workflow。

