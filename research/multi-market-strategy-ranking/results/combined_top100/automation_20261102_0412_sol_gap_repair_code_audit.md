# Trade Test 增量修復稽核｜2026-11-02 04:12 +08:00

## 本輪實際查核
- 已讀取隔離分支 `tools/run_legacy_all_timeframes.py` 與 `src/run_intraday.py` 的現行程式。
- 已重新取得 GitHub Actions SOLUSDT 4h Job 124100610554 日誌，確認 `run_legacy_all_timeframes.py` 執行到 `load_real_ohlcv` 時因五年 K 線不連續而停止。
- 已確認 `restore_gap_klines_from_binance_daily_archive` 存在，會逐個真實 Binance daily ZIP 驗證缺失時間戳，禁止插值造價。
- 已確認重要程式分支：`if gaps and not cache_hit` 才嘗試 daily ZIP 修補；若已有不完整的 cache CSV，則直接拒絕，無法自動修復。此為程式碼中可重現的條件限制，尚未證明本次 Actions job 有 cache hit。
- 另一限制：warm-up 缺口在 gap-repair 前就會報錯；daily 修補僅覆蓋五年窗口內部缺口。
- 請勿直接重跑整批；需先由 log 取得 `BINANCE_ARCHIVE_GAP_DAYS`、`REAL_EXCHANGE_GAP_REPAIR_COMPLETE` 或完整 traceback，再確認是否修補路徑被觸發。

## 本輪成果
- 新跑出五年 OHLCV 策略訊號：0 組。
- 僅舊交易紀錄驗算：0 組。
- 新增 SHA256 驗證：0 份。
- 新增修復：0 個程式修改；完成一項可定位的修補路徑稽核。
- completed/required：跨 Git 與 Actions 全量唯一鍵尚未完成驗證，不報虛構總數。
- 原始 OHLCV、伯努利 iid、Kelly Top100 獨立驗證仍未完成。

## 下一個可執行修復
1. 只在隔離分支修正缺口處理：對不完整 cache 重新驗證並嘗試真實 daily ZIP 修復，若來源缺資料就明記 unavailable；warm-up 同樣必須檢查真實連續性。
2. 先檢查全部 manifest + ranking/trades SHA 及 artifacts，建立 `market × timeframe × family × strategy × exit` 唯一鍵；舊31策略九市場 1d 永久禁止重跑。
3. 真實來源完整且未有已完成配置時，才補跑缺漏 20m 等時區。

## 既有榜單（未更動）
- [38 家族榜](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)

未交 Jules、未新增 workflow、未修改 main、未覆蓋 checkpoint。
