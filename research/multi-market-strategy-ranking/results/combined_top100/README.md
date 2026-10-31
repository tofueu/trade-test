# Trade Test：五年 Python 回測成果與去重進度

**更新：2026-10-31 17:24（臺灣時間）｜狀態：PARTIAL（尚未全部完成）**

## 本次 Git 儲存的實測成果

- 實際五年回測窗口：UTC `2021-10-10 00:00:00` 起，`2026-10-10 00:00:00` 止（不含終點）。
- 僅限使用者指定的 **9 市場 × 17 週期 = 153 個市場週期**。
- 分為 original／compound／fixed／new 四類，完整去重工作清單 **612 批次**。
- **124 批** 已有 GitHub Actions 完成之五年逐筆交易資料，經 SHA256 與本地 Python 績效重算驗證，**12,720 配置，數值差異 0**。
- **488 批尚未達到上述驗證標準**：其中 18 筆既有摘要/日線快照待核、60 筆既有待執行或排隊紀錄、26 筆執行失敗、384 筆目前無已驗證五年分鐘行情。
- **舊策略日線已有結果先核對，禁止無謂重跑。** 已完成且有有效 SHA/逐筆交易的批次直接 `SKIP_RETEST`。
- 「31 舊 + 7 新」與實際 Python 原始碼策略名稱尚有對帳缺口；詳見 [策略碼稽核](strategy_code_audit_20261031.md)，不可將排行榜 38 列直接當成 38 個不同已實作訊號策略。
- 這些 124 批證明 **已存交易紀錄和財務績效可獨立驗算**，不是在此次備份又重新取得所有五年 OHLCV 並執行全部訊號。不能把全部 612 批標記完成。

## 已上傳／保留在此 Git 分支的報告與排名

- [本次備份存證 JSON](python_backtest_upload_checkpoint_20261031.json) — 狀態、各類數量、來源 Git blob SHA。
- [612 批次逐格去重清單](five_year_deduplicated_worklist_17timeframes.csv) — 何者已驗證、跳過、失敗、缺行情。
- [僅指定 9 市場的收益 Top100](local_python_kelly_top100_20261030.csv) — 策略、收益、交易數、Kelly 與交易回放／歷史快照標記。
- [38 家族排名](local_python_38_families_20261030.csv) — 含歷史數據與未驗證來源警示。
- [153 市場週期覆蓋表](local_python_full_market_timeframe_coverage_20261030.csv)。
- [Python 驗算與排錯紀錄](local_python_recheck_20261030.md)。
- [策略源碼稽核](strategy_code_audit_20261031.md)。

原始大型 `trades.csv` / `ranking.csv` 及批次 `manifest.json` 仍以各 GitHub Actions artifact 保存；**本次 Git 小型備份沒有假稱把全部原始逐筆大檔搬入 Git 目錄**。先前 GitHub 發布工作曾因 HTTP 408、ZIP 同名檔案碰撞而失敗；應只補收已成功的工件，不重跑策略。

### 執行限制

Trade Test **禁止交 Jules 1 / Jules 2**、禁止新增 workflows、不修改 `main`。原定每六小時報告 Git + ChatGPT 任務對話。缺真實完整五年 OHLCV 的組合仍標 `unavailable`，不可造價或造績效。
