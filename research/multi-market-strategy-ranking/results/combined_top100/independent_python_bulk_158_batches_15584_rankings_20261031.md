# Trade Test Python 獨立五年收益回放：158 批／15,584 排名配置（2026-10-31）

## 本輪實際執行

先前已以 Python 實測 150 個不重複 (symbol,timeframe,family) 批次、14,816 個排名配置。此次再從 GitHub Actions run `41068912974` 下載並讀取：

1. SOLUSDT 5m，artifact `13001146515`，original / compound / fixed / new 4 分類，384 配置。
2. ETHUSDT 5m，artifact `12997621002`，original / compound / fixed / new 4 分類，384 配置。

兩份 ZIP 的內層 `market-...tar.gz`、各四類 `manifest.json`、`trades.csv` 和 `ranking.csv` 由本地 Python `trade_test_incremental_low2.py` 解壓與讀取。檢查五年 UTC 窗口 `2021-10-10` 至 `2026-10-10` end-exclusive；所有 ranking/trades SHA256 與 manifest 相符。每一排名配置按策略/出場方式，實際風險 pct 與前 N 筆真實 R，以固定初始資金模型 `max(-100, risk_pct * sum(trade_R[:N]))` 重算五年收益。

**增量 8 個不重複分類批次、768 個排名配置全部吻合，0 不一致。去重累計 158 批、15,584 筆配置全部吻合（15,584/15,584），0 解析失敗。** 已檢查另外 ETH 8h/12h/1d/2h/1h/4h/6h 共 28 個分類完整工件，均吻合但與既有驗收集合重疊，所以沒有重複增加完成數。

本次產出完整 158 行去重驗證清單：會話容器 `/mnt/data/TradeTest_incremental_low2_merged_20261031.csv`（此檔案未在本 Git commit 中新增，只在聊天室提供沙盒下載）。

**限制**：這是已生成策略成交紀錄的 Python 獨立收益驗證，而不是全部策略從原 OHLCV 重新生成訊號；未重算每個配置的 Kelly、回撤，尚未補齊 31+7 全部策略碼。此前 Git 124 批和本地 158 批有重疊，不能相加。全 612 分類批次未完成，缺可靠五年行情的項目不得虛構，不動 main，不交 Jules，不新增 workflow。
