# 2026-11-02 03:36 +08:00 — SOL 4h 失敗 stderr 已取得

## 新的可查證修復進展
從既有 GitHub Actions Run #41066783962 的 job **124100610554** 直接取得完整執行日誌（先前曾回報連接器拒絕，此輪重新呼叫成功）。

實際 Python traceback：
```text
run_legacy_all_timeframes.py:210 -> load_market_ohlcv
run_legacy_all_timeframes.py:48 -> intraday.load_real_ohlcv
src/run_intraday.py:153
RuntimeError: Irregular or missing five-year candles; no qualified ranking
```

- Job 的策略執行步驟 6 失敗，後續仍上傳 295-byte 空工件（artifact ID **12983144142**），故 artifact 存在不代表策略成功。
- 日誌顯示下載了 SOLUSDT 4h 月檔（2021-08 至 2026-09）及 2026-10-01 至 2026-10-09 日檔；**不能據此判定確切缺少哪根 K 棒**。
- 現有程式 `run_intraday.py` 已有 `restore_gap_klines_from_binance_daily_archive`，會要求真實 Binance daily ZIP、驗證 timestamp/欄位並保留來源 ZIP SHA；後續需核對此函式是否被執行，以及 gap 判定是在修補之前或之後。
- 下一步應定位 gap 的具體 UTC timestamps、補抓真實 Binance daily archives、驗證完整五年連續性與 OHLCV SHA，僅對缺失的非日線策略執行增量回測；不得以插值補 K。
- 此證據**只適用 SOLUSDT 4h**，不能推定其他 13 個失敗工作的 traceback 相同。

## 本輪嚴格計數
- 新執行五年 OHLCV 策略訊號：**0 組**
- 舊交易回放：**0 組**
- 新 SHA 驗證：**0 份**
- 新增成功取得的失敗工作 stderr：**1 份**
- 全域 completed/required：**未知**（尚未完成跨 Git 與 Actions 的唯一鍵、OHLCV SHA 驗收）
- 舊31策略九市場 1d 禁止重跑，兩份排行榜保留不覆寫；沒有 Jules、新 workflow、main 修改。

## 來源
- [Run #41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962)
- [SOL 4h job #124100610554](https://github.com/tofueu/trade-test/actions/runs/41066783962/job/124100610554)
- [38 家族榜](./local_python_38_families_20261030.csv)
- [Kelly Top100](./local_python_kelly_top100_20261030.csv)
