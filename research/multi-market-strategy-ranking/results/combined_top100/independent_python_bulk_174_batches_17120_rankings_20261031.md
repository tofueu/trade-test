# Python 五年交易紀錄獨立回放驗收 — 174 批／17,120 配置（2026-10-31）

## 本輪新增 2m 實際 Python 驗算（先前大檔超時後改進）

實際在此聊天本機 Python 執行 `/mnt/data/trade_test_2m_incremental_verify.py`；從已下載的 `market-SOLUSDT-2m` (GitHub Actions artifact ID 13015666144) 及 `market-ETHUSDT-2m` (artifact 13012023842) ZIP 工件解壓 tar.gz，採用 **tar 單次展開 + streaming CSV**、按策略/出場方式/目標成交數記錄累積 R，避免將數百萬逐筆交易一次載入記憶體，完成上輪原始策略大 CSV 超時問題。

逐一核對兩個商品、四策略分類 `original,compound,fixed,new` 各 `manifest.json` 的五年時間範圍（2021-10-10 UTC 至 2026-10-10 UTC 不含尾端）、ranking/trades SHA256，並對每筆排名配置按 `max(-100, 實際風險_pct * sum(對應策略/出場方式前N筆真實R))` 重新計算原始固定初始資金五年收益。

| 分類 | SOLUSDT 2m 排名驗算 | ETHUSDT 2m 排名驗算 |
|---|---:|---:|
| compound | 32/32 | 32/32 |
| fixed | 36/36 | 36/36 |
| new | 28/28 | 28/28 |
| original | 288/288 | 288/288 |
| **總計** | **384/384** | **384/384** |

**8 個新去重分類批次、768 配置完全吻合，0 收益不一致、0 SHA 不一致**；比對基準是上輪 166 批／16,352 配置，本輪累計 **174 批／17,120 配置，全部逐筆收益吻合**。去重鍵是 `(symbol,timeframe,family)`，不將重複工件加倍計數。驗證清單 `/mnt/data/TradeTest_incremental_2m_merged_20261031.csv` 含完整 174 行；同會話容器原始 Python 腳本在 `/mnt/data/trade_test_2m_incremental_verify.py`。這些 `/mnt/data` 檔案**是聊天暫存產物，並未由此 MD 檔上傳 Git**。

**重要限制**：本輪驗證的是 GitHub Actions 先前執行並保存的真實逐筆交易 R 和收益公式，**不是直接重生成五年行情與入出場訊號**，也沒有重新獨立計算全部 Kelly 與回撤。既有 Git 124 批與本輪 174 批重疊，不能加總。九商品×17時區×4分類共612批，以及原要求舊31+新7策略碼缺口仍未全部完成。未修改 main、未交 Jules、未新增 workflow。
