# Trade Test 2026-11-02 06:35 +08:00 — runner 路徑與來源核驗

本輪透過已連線 GitHub API，於隔離分支 `report/trade-test-multi-market-20261030` 成功讀取上一輪報告 `automation_20261102_0509_access_and_validation.md`，blob SHA256/Git blob id `6a83030d60f7e3599c6bfebe4e1bf6dce9a98f42`（注意 Git blob SHA-1 不是檔案 SHA256）。同分支讀取 `src/run_intraday.py` 返回 HTTP 404。以 GitHub code search 搜尋 `run_legacy_all_timeframes` 及 `restore_gap_klines_from_binance_daily_archive` 均返回 0 項；搜尋範圍為預設分支，不能據此斷言隔離分支不存在程式。

本輪無法讀取現行 runner、五年原始 OHLCV 或跨工件去重索引，因此未啟動可能重做已完成批次的回測，也未聲稱 runner 已修復。上一輪的人工時間戳檢查僅屬測試，不能當市場訊號。SOL 4h 真實缺口時間戳仍待取得。

- 本輪新跑真實五年策略訊號組合：**0**
- 本輪舊交易回放：**0**
- 本輪新增交易 CSV / 原始 OHLCV SHA256 驗證：**0**
- completed/required：**未核定**（缺少全量 manifest、trade CSV、artifact 交叉去重）
- 38 家族榜：沿用既有歷史榜，未更新
- Kelly Top100：沿用既有歷史榜，未更新，不能當作全數已驗收
- 舊31策略 × 9市場 × 1d：**禁止重跑**，本輪未重跑
- 無 Jules、無新 workflow、未修改 main

下一步：透過隔離分支 Git tree 列出 runner 真實路徑（避免盲猜），收齊 manifest/CSV/artifact 建立 `market×timeframe×family×strategy×exit` 去重清單，再驗證真實五年 K 線及 SOL 缺口，僅對未完成配置執行既有 Python runner。

[38 家族歷史榜](local_python_38_families_20261030.csv) | [Kelly Top100 歷史榜](local_python_kelly_top100_20261030.csv)
