# Trade Test｜當前工作狀態與交接基準（2026-11-01，台灣時間）

> **未完成；此文件是進度與事實整理，不是新增回測成果。** 只保存到 `report/trade-test-multi-market-20261030`，不變動 `main`。

## 1. 使用者最終要求（優先）

- **直接在 ChatGPT Python 執行**真實五年行情上的完整策略訊號回測。不能把 GitHub Actions / Jules 當作替代執行，也不要只監控、重播舊 trades 後聲稱新測試完成。
- **已完成的舊策略日線（1d）不要重測**；依策略、商品、時區唯一鍵去重，保留有證據的既有結果。舊策略補測其他 16 時區，新策略缺什麼補什麼。
- 指定市場（**9**）：`BTCUSDT`、`ETHUSDT`、`SOLUSDT`、`GC=F`、`SI=F`、`ES=F`、`NQ=F`、`^TWII`、`USDJPY=X`。
- 指定週期（**17**）：`1m, 2m, 3m, 5m, 10m, 15m, 20m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 8h, 12h, 1d`。
- 五年 UTC 計算窗口：`2021-10-10 00:00` 至 `2026-10-10 00:00` **exclusive**。任何合成週期只能由可靠真實且連續的基礎 K 棒重新聚合，禁止虛構缺口。
- 先逐組完成真實程式執行、保存逐筆交易、策略統計與排行榜；每小時版本化備份進原 Git 隔離分支。使用者要求錯誤時主動改道、不要一遇錯就回報結案或要求再次手動授權；**不等於目前 Python 能夠在 ChatGPT 訊息結束後持續常駐執行**。
- 評比重點包括五年 **≥70 筆交易、收益 >100%、Kelly 風控、勝率、交易數、總收益、年化、最大回撤、止損數、盈虧比**。不符合應顯示實際結果而非刪掉證據。
- 策略**總數尚有矛盾必須對帳**：先前工作規格和 2026-10-31 報告寫「舊 31＋新 7」=38；後續對話提「舊 30＋新 7」=37，最近又明確要求「總共 40」。**不能把 37、38 或 40 偷換成另一數字，也不能以改名/複製新策略來湊。** 以 40 為未收斂目標，待完整原策略規則對帳。40×9×17=6,120 是**理論組合上限，不是目前已可執行策略數**；舊 30×9×1d=270 是假設 30 個舊策略在全部市場已有可用日線結果才可跳過的理論數，**不可無證據直接認定 270 個均已驗收**。

## 2. 已有程式與歷史證據

- 原始行情取得與驗證：`src/run_intraday.py`，Binance USD-M `data.binance.vision/data/futures/um` 月度 ZIP＋2026/10 初每日 ZIP；嚴格驗證 K 棒、補缺來源、快取 `src/five_year_market_data/intraday`；衍生 `2m,10m,20m,45m,3h`。其他市場 1d 是 `src/five_year_multi_market_kelly.py` 的 Yahoo Finance 來源，分鐘級未具完整五年資料證據。
- 主要信號回測程式：`tools/run_legacy_all_timeframes.py`；分類 `original`（8 個策略槽）、`compound`（8）、`fixed`（9）、`new`（7）。**舊 25 個分類內槽位、但相同名稱跨分類重複，舊名稱只有 24 個不重名，＋新 7 個不重名。**「策略槽位」「策略名稱」「四個 family」「配置/出場法」**不是同一統計單位**。
- Git 歷史盤點 `codex/all-prior-strategies-inventory-20261020:research/all-strategy-inventory/README.md` 提及另 5 種曾報 H1 的策略：`Ichimoku Kijun/Cloud`、`DMI_ADX20`、`WilliamsR_EMA200`、`CCI20_EMA200`、`ROC10_EMA200`。該盤點認定**找不到可重現的程式、K 線 manifest 與逐筆工件**，只能列待恢復/實作，**不是已補齊 5 策略的可執行程式**。
- 舊 Git 歷史每日線總榜有 **9,556 列、32 種訊號規則、26 商品**（跨不同商品/出場配置的排名資料）；不得直接與目前 9 市場及全部 17 時區混算。
- 現有保存的實際歷史策略 `trades.csv`、`ranking.csv`、`manifest.json`、`checkpoint.json` 工件可供審計。2026/10/31 的 ChatGPT Python 從這些工件去重並**獨立重算 188 個 (symbol,timeframe,family) 批次、18,592 筆排名配置，收益重播一致**。**這是已存交易的績效核對，不是本地重新產生原始 OHLCV 策略訊號；不能稱 188 組策略已新跑完。**
- `9 市場×17 時區×4 family = 612` 只是分類覆蓋的盤點單位（**不是策略數**）。188 個去重交易結果驗算分類批次，另 **424** 分類批次缺同級證據；其中 **384 = 6 個非加密市場×16 日內週期×4 分類**，另 40 其他來源/工件缺口（包括 **20m 全 9 市場×4 分類=36**）。個別分類已有日線快照或舊報告，待驗證不能一律推論曾完整執行或從零重跑。
- 日線既有 Kelly 公式核對 3,460 筆配置無公式不合，**不等於全部策略都符合 Kelly、≥70 筆、>100%**；完整回撤/出場也尚未逐組重建。

## 3. 已確認資料來源阻礙（須修復，而不是當作完成）

- Git 本分支沒有 `src/five_year_market_data/` 原始行情快取目錄（contents API 404），之前 233 MB 的原始回測打包工件（Actions run `41064675326`, artifact `12990575827`）檢查了 **154 個檔名，無原始 OHLCV/klines/candles CSV**。已查過的 ZIP 主要存的是交易、排名、驗證結果。
- 在這個 ChatGPT Python 容器，先前對 `data.binance.vision`、`raw.githubusercontent.com`、`query1.finance.yahoo.com` 直接連線，出現 `gaierror [Errno -3] Temporary failure in name resolution`；改走 S3/其他下載路徑未成功取得資料。**Jules 曾可下載，不代表本聊天環境有相同網路權限**。
- 遇到無法存取的五年真實資料，狀態必須是 `UNAVAILABLE/UNVERIFIED`、保留原因與原始 URL，不可插值造 K 棒、補假交易或用合成走勢填測試。
- **最後可核實新增原始五年 OHLCV 信號回測完成數：0**；目前也沒有 40 個完整策略規則與 9 市場×17 週期全數完成的可驗證證據。**不宣稱專案已完成**。

## 4. 接手執行規則

1. 先按當前 Git 真實策略定義逐一對帳，不要改名湊 40；找出歷史其餘策略規則/程式，留明確缺口清單。
2. 確認行情已取得與保存來源、交易所、商品合約、UTC 起訖、連續性與散列值。對 BTC/ETH/SOL 優先重用 Binance 月/日 ZIP 或合格鏡像；對非加密日內五年行情須先核對來源可用性、交易時段與合約連續化方法。
3. 依策略×市場×時區去重，**舊策略既有 1d 禁止重跑**，其他已有完整真實回測證據者跳過，只實測未完成的；先補可執行的分鐘/衍生時區，逐組落盤真實成交、成本、回撤、止損、Kelly 與 manifest。
4. 每批完成保存 `trades.csv`、`ranking.csv`、`checkpoint.json`、`manifest.json`、資料來源證明；把可驗證新增測試成果上傳現有隔離分支，**Git 僅備份、不代替 Python 回測**。若環境無法持續常駐，不得宣稱背景執行中。
5. 直到策略定義、行情可用性與所有可執行組合正式逐格驗收，才可出最終 Top100 與未達標、資料不可用原因列表；之前不得標 `COMPLETE`。

## 5. 參考 Git 原始報告

- `strategy_code_audit_20261031.md`：原始策略名單/槽位與 612 分類矩陣。
- `five_year_deduplicated_worklist_17timeframes.csv`：原有分類去重清單（不得當 40 個實際策略）。
- `independent_python_bulk_188_batches_18592_rankings_20261031.md`：188 批已存交易收益回播驗證。
- `kelly_daily_and_424_missing_audit_20261101.md`：Kelly 算式及 424 缺口。
- `raw_ohlcv_recovery_inspection_20261101.md`：行情下載阻礙、歷史打包工件檢查。
- `research/all-strategy-inventory/README.md`（在 `codex/all-prior-strategies-inventory-20261020` 分支）：歷史缺漏 5 H1 策略證據。
