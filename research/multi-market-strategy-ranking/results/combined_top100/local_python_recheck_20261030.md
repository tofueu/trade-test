# Trade Test — Python 五年回測與六小時驗收進度
更新日期：2026-10-30（臺灣時間）。**任務未完成，禁止把驗算或排隊作為全策略通過。**

## 執行規則
- **Trade Test 舊31＋新7策略不得交給 Jules 1、Jules 2 或 AI Orchestrator 的 Jules 派工**；七專案自動化的原舊派工規則已修正。
- **不新增 GitHub workflow、不修改 main、不重新跑已有完整並通過 SHA256 的昂貴批次**。使用既有 Python 程式及真實已完成 Python artifacts。
- 每六小時在現有 Git 分支此報告更新進度，並由 ChatGPT 自動任務提供繁體中文回報；每輪即使進度為 0 也列出實際故障和未完工項目。

## 本輪真正執行的本機 Python
- 用完整 `manifest.json`、`ranking.csv`、`trades.csv` 驗證批次 SHA256，逐筆重算風險、前四年 IS Kelly、交易數、五年收益與權益回撤。
- 已驗證 **90 個已完成批次、9,328 種策略／倉位／出場配置**；收益／Kelly／回撤／交易數不一致 **0**。
- 自前次 85 批、8,908 配置增加：**BTCUSDT 1m 固定出場 1 批＋36 配置**（[來源工件](https://github.com/tofueu/trade-test/actions/runs/41064675326)）；**ETHUSDT 5m original、compound、fixed、new 四批＋384 配置**（[來源工件](https://github.com/tofueu/trade-test/actions/runs/41066783962)），皆實際用 Python 重新驗算，未重算完整 OHLCV 進出場訊號。
- 全部 **38 種策略家族**仍在榜，包括未達最低筆數者；其中 **20** 家族最佳配置仍來自無法在此本機逐筆核對的歷史快照。
- **收益 Top100**：≥70 筆真實成交、總收益 >100%、風險 ≤前四年 IS Kelly 且不超過 100% 回撤，依 商品＋週期＋策略＋出場去重；**72** 筆本機逐筆重新驗算、**28** 筆歷史快照（必須標記來源）。本輪新增五批沒有改變 Top100。
- **九市場×25 週期＝225 對**；可供本機使用真實逐筆交易驗算的 **26** 對、其中 **14** 對具備四類（original、compound、fixed、new）回測紀錄。未驗證的週期／市場不算完成。
- Bernoulli IID 假設**未獲證明**；未作 TradingView／Pine 逐筆對照。

## 遠端既有 Python 執行、資料限制
- BTC 五年 12 週期×三種舊分類，GitHub run [41064675326](https://github.com/tofueu/trade-test/actions/runs/41064675326)：本輪查到 **34/36 成功、2 個 1m（original、compound）仍在執行**。不要把進行中算完成。
- 多市場 run [41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962)：本輪查到 **14 成功、14 失敗、2 執行中**；後續修復版本待確認是真正跑過，而非只提交程式。
- SOL 2022 年少 K 線，已確認能從 Binance 同一商品的原始 daily ZIP 取得實際歷史 bar，保留 ZIP SHA256；**資料補齊≠策略回測完成**。
- USDJPY Yahoo 有 75 根不合高低價關係 K 線，其他來源尚未完成相同五年資料驗證；台灣指數的農曆春節非交易日不能補成假價格。
- 目前聊天 Python 容器無法直接連線取得整套五年 OHLCV，所以本地的真正工作是**逐筆交易管理重演**；不是所有市場與週期的信號產生器全量重回測。未取得原始行情的列都應標記 `unavailable`。

## 同步檔案
- `local_python_kelly_top100_20261030.csv`：含歷史來源註記的原有 Top100（本輪榜單未變）。
- `local_python_38_families_20261030.csv`：全部 38 家族（本輪家族最佳未變）。
- `local_python_full_market_timeframe_coverage_20261030.csv`：本輪 BTC 1m 與 ETH 5m 的**本機逐筆驗算覆蓋**已更新。
- `latest_verification_manifest.json` 是 GitHub CI 曾提交的較舊快照，**不能因本機回放 90 批就冒稱此 manifest 已涵蓋全部**。需持續收集實際成功 artifacts 並重建。
