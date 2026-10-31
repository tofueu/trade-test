# Trade Test 五年 Python 獨立逐筆收益回放 — 182 批、17,888 排名配置（2026-10-31）

## 本輪實際完成

本次直接在 ChatGPT Python 容器完成 GitHub Actions #41068912974 的四件大體積交易工件的本地逐筆檢查：
- SOLUSDT 2m artifact `13015666144`
- ETHUSDT 2m artifact `13012023842`
- SOLUSDT 1m artifact `13013451517`
- ETHUSDT 1m artifact `13005109289`

所有工件包括 original、compound、fixed、new 四類策略。分別核對 `manifest.json` 的完整五年窗口（UTC 2021-10-10 至 2026-10-10 end-exclusive）、`ranking.csv` 和 `trades.csv` SHA256，然後根據每筆原始交易 `R` 逐筆累計收益，用原回測的固定初始資金風險模型 `max(-100, 實際風險_pct * sum(對應策略/出場方式前N筆R))` 驗算全部配置，容忍度 1e-6 個百分點。

### 1m 和 2m 新增成果
| 市場時區 | original | compound | fixed | new | 合計驗證配置 |
|---|---:|---:|---:|---:|---:|
| SOLUSDT 2m | 288 | 32 | 36 | 28 | 384/384 |
| ETHUSDT 2m | 288 | 32 | 36 | 28 | 384/384 |
| SOLUSDT 1m | 288 | 32 | 36 | 28 | 384/384 |
| ETHUSDT 1m | 288 | 32 | 36 | 28 | 384/384 |
| **合計** | **1,152** | **128** | **144** | **112** | **1,536 / 1,536** |

1m original 大檔：SOLUSDT 原始 5,907,627 筆存檔逐筆交易，ETHUSDT 6,062,958 筆。兩者已透過 Python 一次展開 TAR + 串流 CSV（避免整檔進記憶體）、單分類重試與目標成交數 prefix-R 累計，完成 288/288 配置各自核對，不再有超時未驗的部分。其餘 1m/2m 六個分類也各 SHA/收益一致。

本輪前 166 批／16,352 配置；新增 16 個不同的 (symbol,timeframe,family) 分類批次，增加 1,536 筆排名配置，**去重合計 182 批／17,888 配置，17,888/17,888 五年收益驗算吻合，0 SHA 不一致、0 收益不一致**。未將和前批重複的工件加倍計數。

原始執行腳本在本對話容器 `/mnt/data/trade_test_2m_incremental_verify.py`、`/mnt/data/trade_test_1m_finish_others.py`，完整去重 CSV `/mnt/data/TradeTest_incremental_1m_merged_20261031.csv`（182行）。這些聊天沙盒檔案**尚未藉此文字報告複製到 Git**，避免把報告當成上傳整份 CSV。

**限制與未完成範圍**：這是前次已由策略程式產生的五年成交工件的獨立逐筆收益重算，**不是新取得原始 OHLCV 再重發入出場訊號**。未全面獨立重算 Kelly、最大回撤；完整 9 市場×17時區×4分類的612批仍未全部有合格五年行情/成果；需求中的31舊+7新策略碼仍有缺口。以前 Git 124 批集合與此處 182 批重疊，不能相加。不得標為全案完成。不使用 Jules、不動 main、不新增 GitHub workflow。
