# Trade Test 2026-10-31 Python 回放：166 批、16,352 筆配置

在前輪已驗 158 個不同 (symbol,timeframe,family) 分類批次、15,584 配置之上，從 GitHub Actions run 41068912974 另外取回 SOLUSDT 3m artifact `13000344753` 和 ETHUSDT 3m artifact `12997545847`，直接在本地 Python 執行 `trade_test_incremental_3m.py` 解壓 ZIP / tar.gz，驗證每一分類 `manifest.json`，並獨立重算逐筆 trade R 與全部配置的五年收益。

**兩個時區各有 original / compound / fixed / new 四類、每市場 384 筆配置；新增 8 批、768 筆配置，768/768 完全吻合，0 不一致。去重合併至上一輪 158 批之後，累計 166 批、16,352 筆配置，16,352/16,352 全部吻合。**

計算與比對：五年 UTC 2021-10-10 至 2026-10-10 (exclusive)，每份 ranking.csv / trades.csv SHA256 與來源 manifest 相符；按 `(策略,出場方式)` 分組，依五年交易數取前 N 筆 R，使用實際風險_pct，按照原始**固定初始資本線性風險**收益口徑 `max(-100, risk_pct * sum(R[:N]))`；容差小於 1e-6 百分點。原始下載工件與去重資料都保持不變。

本輪有明確處理批次去重基準：初次試跑引用了 150 批舊清單，只能得出 158 批，**不採用**；更新成 158 批的最新本地清單後完整重算，得到 166 批／16,352 配置，0 不一致。驗證清單在本次會話容器 `/mnt/data/TradeTest_incremental_3m_merged_20261031.csv`（166 行），這個暫存 CSV 尚未提交到 Git。

本次驗證為既有真實五年交易工件的**獨立收益回放**，而非重新從原始 OHLCV 計算入出場訊號。沒有宣稱全面獨立重算 Kelly、最大回撤；沒有把 166 與先前 Git 124 批相加（兩集合重疊）。所有 9 市場×17 時區×4 分類 612 批和舊31＋新7全策略仍**未完成**；未交 Jules，未動 main，未新增 workflow。
