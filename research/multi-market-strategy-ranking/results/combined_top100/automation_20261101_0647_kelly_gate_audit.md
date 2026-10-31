# Trade Test 2026-11-01 06:47 +08 — 九市場榜風險門檻實際稽核

本輪直接讀取既有隔離分支 `automation_20261101_0621_nine_market_family_snapshot.csv`，逐列檢查收益、交易筆數、IS Kelly 與實際風險，未改寫原排行榜。

## 可重現規則
`eligible = (five_year_return_pct > 100) and (trade_count >= 70) and (actual_risk_pct <= IS_Kelly_pct + 1e-8)`。此規則僅篩選歷史快照，**不代表獨立原始 OHLCV 訊號回測或完整五年來源驗證**。

## 實際發現
- 九市場歷史家族快照僅 **30 列**；其餘 8 家族的九市場代表尚缺，不能稱為完整 38 家族榜。
- 其中 **2 列違反實際風險 <= IS Kelly**：
  - 原榜第 2 名 SOLUSDT 2h `Supertrend+EMA200`：實際風險 10%，IS Kelly 8.234485925872256%，交易 600，收益 1836.6047786867057%。
  - 原榜第 6 名 SOLUSDT 2h `Supertrend10_3`：實際風險 10%，IS Kelly 6.442751124985804%，交易 476，收益 1234.6509528930983%。
- 30 列中僅 **10 列**符合上述三項數值門檻；仍須驗證五年 OHLCV、策略訊號、交易 CSV 及來源 SHA 才能列入正式 Top100。
- 其中 **16 列是 1d**，舊日線只保留歷史基準，禁止重新跑。
- 原榜第 10 名 SOLUSDT 1d `Donchian20_Volume_EMA200` 雖收益 848.73%，但交易僅 27 筆，不能進門檻榜。

## 本輪新增實測及限制
- 新從五年真實 OHLCV 產生入出場策略訊號：**0 組**。
- 新驗證成交回放：**0 組**；新驗 SHA：**0 批**。
- 原因：本輪 GitHub connector 可讀既有 CSV，但未取得可供 Python 執行的五年 OHLCV 及對應策略實作；不以歷史交易重播充當新回測。
- 最新逐策略 × 市場 × 時區 × 出場的 completed/required 尚無可靠完整數字，先不沿用 124/612 作為完成率。
- 下一個可執行修復：先取得 BTC 1m original/compound、ETH 1m/3m/5m ZIP 及真實 5m OHLCV，校驗 manifest/CSV/K線 SHA；按已完成 key 去重，對真正缺失的 20m 組合用四根連續真實 5m K 棒跑原 Python 訊號。
- 不得將上述兩筆 Kelly 超額風險交易列為符合條件的 Top100；也不得將九市場快照的 30 列宣稱完整 38 家族。

原始榜：[38 家族](local_python_38_families_20261030.csv)；[Top100](local_python_kelly_top100_20261030.csv)；[九市場快照](automation_20261101_0621_nine_market_family_snapshot.csv)。

未交 Jules，未新增 workflow，未修改 main。
