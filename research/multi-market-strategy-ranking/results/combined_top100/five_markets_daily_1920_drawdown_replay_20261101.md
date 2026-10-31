# 2026-11-01 Python 獨立重算五市場日線五年最大回撤（1,920 配置）

本次在本地 Python 直接執行 `/mnt/data/trade_test_daily_dd_verify.py`，讀取先前從 GitHub Actions 下載的五個市場 `GC=F`（黃金）、`SI=F`（白銀）、`ES=F`、`NQ=F`、`^TWII` 日線真實交易工件。

每市場包含 original（288 配置）、compound（32）、fixed（36）、new（28），合計 384；五市場合計 **1,920 筆排名配置**。對各工件 `manifest.json` 的 `ranking_sha256` 與 `trades_sha256` 做真實檔案 SHA256 比對；按策略/出場方式重組逐筆 R，以排名配置的實際風險_pct 及五年交易數，在固定初始本金倉位口徑下逐筆算 `equity=max(0,equity+risk_pct*R)`、`peak=max(peak,equity)`、`drawdown=(peak-equity)/peak*100`。

**GC=F 384/384、SI=F 384/384、ES=F 384/384、NQ=F 384/384、^TWII 384/384 全數吻合，總計 1,920/1,920；最大數值誤差 8.1713e-14 百分點（浮點捨入級別）。**

本輪完整 Python 結果保存在本對話容器 `/mnt/data/TradeTest_5_markets_daily_drawdown_20261101.csv`，1,920 列含 reported_dd、computed_dd、abs_error。這是先前已保存五年工件的**新增獨立最大回撤驗算層級**，不是 1,920 個新回測訊號組合，**不得把已完成批次從 188 虛加**。

本輪另完成 BTCUSDT 新策略 2m/10m/45m/3h 共 112 配置最大回撤驗證（另見同分支 `BTCUSDT_new_strategy_4timeframes_drawdown_replay_20261101.md`）。整體 9 市場×17 時區×4 類 612 批中，此前本地 188 批已有交易收益回放，剩餘 424 批欠缺相同驗收。缺完整五年日內行情的 384 批不可編造；BTC 新策略其餘時區、20m 和 USDJPY 日線等仍待取得真實資料/可運作原始策略程式。沒有交 Jules、沒有動 main、沒有建立新 workflow；本報告不代表全數完成。
