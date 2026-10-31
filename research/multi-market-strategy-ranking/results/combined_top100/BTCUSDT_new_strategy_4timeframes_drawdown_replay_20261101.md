# BTCUSDT 新策略最大回撤獨立 Python 重算 — 2026-11-01

本輪未重跑任何已完成的五年策略訊號。直接在本對話 Python 容器執行 `/mnt/data/trade_test_dd_verify.py`，讀取先前已從 GitHub Actions 下載、目前仍持有的四份五年真實交易工件：

- BTCUSDT 2m / new：28 個配置；
- BTCUSDT 10m / new：28 個配置；
- BTCUSDT 45m / new：28 個配置；
- BTCUSDT 3h / new：28 個配置。

每個工件均獨立核對其 `manifest.json` 內 `ranking_sha256` 和 `trades_sha256`。按 `策略 + 出場方式` 分組從 `trades.csv` 取得前 `五年交易數` 筆逐筆 R；對應每列排名的 `實際風險_pct` 以固定初始資本方式重建權益曲線：`equity = max(0, equity + risk_pct * R)`，以 `(peak-equity)/peak * 100` 計算歷史最大回撤百分比並與原 `五年最大回撤_pct` 比較。

**結果：112/112 配置的五年最大回撤獨立重算吻合，0 不一致，最大絕對誤差為 0（CSV 所列保留 9 位小數）**。完整核對檔已在本會話容器 `/mnt/data/TradeTest_BTC_new_drawdown_independent_20261101.csv` 產生，可供本對話下載。該 CSV、腳本並未隨此 Markdown 文檔直接提交 Git。

本次工作同時將本地已完成去重清單和剩餘 424 分類清單重新對照：BTCUSDT 新策略已驗 2m、10m、45m、3h 四個時區（另 13 個時區新策略缺漏）；BTC 尚有原始/複合/固定策略缺漏；ETH/SOL 主要缺 20m；非加密六個市場 16 種日內時區需要可靠五年實際 OHLCV。GitHub run 41064675326、41066783962、41068912974 中未發現可下載的新 20m 與 BTC 1m new 工件，USDJPY 1d 工件僅約 300 bytes，不能視作成功交易記錄。

**重要：** 這是對已存五年交易的最大回撤獨立驗算，**不是新增 112 筆策略或補齊剩餘 424 批**。已驗 188／612 分類批次和未驗 424／612 分類批次保持不變。尚未完成全策略、全部五年資料與 31 舊＋7 新策略碼規格，不能標註完成。保留 Git 隔離分支；不動 main、不交 Jules、不建立 workflow。
