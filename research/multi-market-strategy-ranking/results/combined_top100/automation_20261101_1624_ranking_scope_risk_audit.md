# Trade Test 2026-11-01 16:24 +08:00 — 排行榜範圍與風險門檻重新稽核

本次直接從隔離分支讀取三份 CSV，以欄位名稱計算筆數、指定九市場範圍及實際風險 > IS Kelly（浮點容忍 1e-8）。這是**既有排名 CSV 的欄位驗算**，不是五年原始 OHLCV 策略訊號回測，也沒有驗證 K 線 SHA。

| CSV | 列數 | 非指定市場列 | 風險 > IS Kelly 列 | iid已證明列 |
|---|---:|---:|---:|---:|
| all_strategy_families_ranked.csv | 38 | 10 | 3 | 0 |
| local_python_38_families_20261030.csv | 38 | 8 | 2 | 0 |
| local_python_kelly_top100_20261030.csv | 100 | 0 | 0 | 0 |

關鍵問題：兩份 38 家族歷史榜含非指定市場；不能直接作為九市場正式全家族榜。Top100 CSV 雖沒有非指定市場或超過 IS Kelly 的數值列，但 100 列中 iid已證明=0；不能稱 iid 已驗證，也不能從排名 CSV 直接推定五年原始 K 線訊號重跑完成。

處理：保留原 CSV 不覆蓋，正式榜需從逐筆交易來源、manifest、原始行情 SHA 及完整唯一鍵 (market,timeframe,family,strategy,exit) 重建。舊31策略×全部9市場×1d 禁止重跑；既有工件先驗收。BTC 1m original/compound 與 ETH 1m/3m/5m 優先；20m 只用連續真實 5m 四根聚合。非加密五年分鐘資料缺證據標記 unavailable，絕不補假 K 線。

本輪新跑出策略訊號：**0 組**。本輪舊交易紀錄回放：**0 組**。本輪 CSV 欄位稽核：**3 份**。新驗原始 OHLCV SHA：**0**。逐策略 completed/required：**無法由這三份榜單可靠確定**。

不交 Jules、不新增 workflow、不動 main。完整回測尚未完成。
