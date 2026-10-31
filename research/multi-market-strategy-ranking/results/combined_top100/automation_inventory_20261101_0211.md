# Trade Test 增量工件與未驗收批次核查 — 2026-11-01 02:11 Asia/Taipei

本次直接以 GitHub connector 讀取現有 `five_year_deduplicated_worklist_17timeframes.csv`（612 列），並重新查詢既有 Actions #41064675326、#41066783962、#41068912974 的 artifacts。這份清單是 **2026-10-31 的歷史基準，不是最新 138 批本地 SHA 稽核清單**；不得以 124 與 138 相加。

| 既有工作清單狀態 | 分類批次 |
|---|---:|
| COMPLETE_5Y_GIT_SHA_AND_LOCAL_TRADE_REPLAY | 124 |
| NEW_7_RESULTS_PRIOR_GIT_SUMMARY | 12 |
| EXISTING_RUN_QUEUED_OR_ACTIVE | 24 |
| PENDING_FULL_FIVE_YEAR_PYTHON | 36 |
| FAILURE_ARTIFACT_NO_RESULTS | 26 |
| NO_VERIFIED_FIVE_YEAR_INTRADAY_SOURCE | 384 |
| LEGACY_DAILY_DONE_PRIOR_ARCHIVE | 6 |
| **合計** | **612** |

**注意**：此歷史清單的 QUEUED_OR_ACTIVE 是當時狀態，不能當成今日仍在執行。先前本地 ZIP SHA 掃描已報告 138 個去重完整工件；尚需將這 138 筆和此 612 列基準按 market/timeframe/family/exit/strategy 逐一合併，避免誤計。

既有 Actions artifact 第一頁：#41064675326 有 37 份、#41066783962 有 31 份、#41068912974 有 43 份。ETHUSDT 1m/3m/5m 在 #41066783962 和 #41068912974 均找到未過期 artifacts（分別約 151MB、49MB、29MB），應按 SHA 去重，**不得把兩個 run 的同名 artifacts 當成不同完成批次**。BTC 1m original/compound 先前已核對 SHA，應保留有效工件，不重跑。

本次 connector 僅返回 artifacts 名稱與大小，**未取得這六份 ETH ZIP 內交易 CSV、manifest 內容**，因此本次新增已驗證成交回放 **0**、新增五年 K 線訊號回測 **0**。本次沒有真正執行策略 Python、沒有更新績效排行，現有榜單保留。阻礙是 GitHub connector 的 artifact metadata 不能替代 ZIP 下載與檔內 SHA 驗證；下一輪應透過可下載的 artifacts 或已存在本地 ZIP，優先合併 ETH 1m/3m/5m，並排查 20m 與缺漏的舊策略程式定義。

範圍嚴守 9 市場、17 週期，目標 31 舊+7 新；理論 5814 個市場×週期×策略（尚未考慮各策略出場）。目前 runner 的舊策略定義槽不足 31 個，不可假裝 38 種獨立策略已完整實作。非加密市場缺完整五年分鐘線 384 個分類批次維持 unavailable。舊日線不重跑；SOL 僅允許真實 Binance daily archive 修復，禁止合成缺口；伯努利 iid 尚未證明。

兩份既有排行榜（**非本輪新產出**）：
- [全策略家族 CSV](local_python_38_families_20261030.csv)
- [Kelly 五年收益 Top100 CSV](local_python_kelly_top100_20261030.csv)

沒有動 main、沒有新增 workflow、沒有交 Jules，也沒有覆蓋 checkpoint。
