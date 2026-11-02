# Trade Test — 2026-11-02 16:25 +08:00

## 本輪實際修復
- 修改既有隔離分支 `research/multi-market-strategy-ranking/src/run_intraday.py`，commit `ccf852426d3bb3ef96760d385386b8cee1dae1f6`。
- 在五年首尾覆蓋檢查前，對缺失的窗口邊界與指標 warm-up 邊界，嘗試下載同交易所、同商品、同週期的 Binance 真實 daily ZIP K 線。所有修補仍通過既有 OHLCV、時間戳、缺失根數與 SHA receipts 稽核；超過原本 20 天／24000 根安全門檻則拒絕，不補造 K 棒。
- 將邊界修補 receipt 併入內部缺口修補的來源記錄；已存在快取且修補成功時，保留原子更新條件。
- 本次為**原始碼修復提交**，未能在此環境取得私有 repo 原始程式的本地可執行副本，無法宣稱已通過 Python 編譯、SOL 真實 ZIP 下載、整體五年連續性測試或策略回測。需在下輪優先實測。

## 完成口徑
- 本輪新增五年 OHLCV 策略訊號：**0 組**。
- 本輪僅舊交易回放：**0 組**。
- 本輪新增實體 CSV SHA 驗證：**0 份**。
- 新增程式修復：**1 檔**。
- completed/required：尚未核定，不能以九市場×25週期估算。
- BTC 1m original/compound、ETH 1m/3m/5m：保留前輪 SHA 驗收，禁止重跑已完成配置。
- 舊31種策略的九市場 1d：全部禁止重跑。
- 448 個未保存出場：仍須逐一對照 ranking/trades/manifest，不得視為448個新策略回測。
- 無 Jules、無新 workflow、未動 main。

## 下輪可執行驗收
1. 對修改後 runner 執行 `python -m py_compile`，使用真實 SOLUSDT Binance daily ZIP 核對邊界及 warm-up，確認 5 年 K 線完整、OHLCV SHA。
2. 優先建立 manifest + ranking + trades 的唯一鍵去重清單，僅執行真正缺失且有真實五年資料的配置。
3. 完成交易明細、風險<=IS Kelly、70筆及收益>100%後才更新 Top100。

[38策略家族既有排行榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)

[Kelly Top100既有排行榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
