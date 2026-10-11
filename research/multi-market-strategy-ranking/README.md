# 五年多市場策略研究與收益排名

這個資料夾整理每日線多市場策略的回測程式、做單條件與排名結果。此研究資料夾獨立於 SMC 多時區回測與 AI 控制面板；內容透過單獨分支提交，待審查後再決定是否合併。

## 回測範圍

- 期間：2021-10-10 至 2026-10-10，UTC；OOS 為最後一年（2025-10-10 至 2026-10-10）。
- 市場：7 個加密貨幣永續商品、7 組外匯、12 個傳統期貨連續合約，共 26 個商品。
- 行情來源：Binance USD-M 日線與 Yahoo Finance 日線。期貨使用資料商連續合約代碼，不能視為逐月換倉或真實合約成交記錄。
- 訊號在日線收盤確認，下一根日線開盤進場。初始止損為 1.5 ATR；若同一根日線同時觸及止盈與止損，採保守的止損先成交假設。
- 交易成本採研究估算：加密貨幣每邊 5 bps 滑價及 5 bps taker 費；外匯以 0.4 pip/邊估計；傳統期貨以每邊 1 tick 加每口 2.5 美元手續費估算。實際點差、資金費率、合約規格與成交差異未完全建模。

## 新增的七種策略與做單條件

| 策略 | 進場 | 出場／止損止盈 |
|---|---|---|
| Turtle55_20_EMA200 | 收盤突破前 55 日高／低，並位於 EMA200 同方向 | 反向突破前 20 日通道退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| Supertrend_ADX20 | Supertrend(10,3) 翻多／翻空，且 ADX14 > 20 | Supertrend 反向退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| EMA20_50_ADX20 | EMA20/EMA50 黃金交叉／死亡交叉，且 ADX14 > 20 | 反向交叉退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| Keltner20_1.5ATR_EMA200 | 收盤突破 EMA20 ± 1.5 ATR 通道，並符合 EMA200 趨勢方向 | 收盤回到 EMA20 另一側退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| BB_Reentry_RSI_ADX25 | ADX14 < 25 時，收盤由布林 2σ 外回到帶內；RSI14 < 45 做多、> 55 做空 | 回到布林中軌退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| Donchian20_Volume_EMA200 | 成交量 > 20 日均量 1.5 倍時突破前 20 日通道，並符合 EMA200 方向 | 反向突破前 10 日通道退出；另設 1.5 ATR 初始 SL 與固定 R TP |
| MACD_EMA200_ADX20 | ADX14 > 20 時 MACD 與訊號線交叉，且收盤符合 EMA200 趨勢方向 | MACD 反向交叉或 EMA200 趨勢失效退出；另設 1.5 ATR 初始 SL 與固定 R TP |

新增策略程式測試止盈候選 0.75R、1R、1.5R、2R、3R，以前四年 IS 的收益／回撤選擇每個「商品 × 策略」的止盈目標，之後才計算五年與 OOS 成績。因此新增策略結果表列的是 IS 選出的 TP，不是五種 TP 候選的完整交叉表。

## 倉位法與收益欄位

每個測試組合計算四種倉位法：固定 1R（初始本金的 10%）、全凱利、半凱利、四分之一凱利。凱利比例由前四年 IS 的交易結果估計。單筆風險金額固定以初始本金計算，收益採逐筆損益加總，不按每筆結餘複利。

- `五年收益_pct`：2021-10-10 至 2026-10-10 全期的模擬累積收益。
- `五年最大回撤_pct`：以模擬帳戶權益計算的最大回撤。
- `OOS收益_pct`：最後一年模擬收益。
- `五年交易數`、`固定止盈數`、`止損出場數`：成交筆數及出場原因統計。
- 同一策略與商品會因不同出場方式、止盈目標或倉位法出現多列；總排名不代表去重後的策略數。

## 檔案

- `src/run_strategies.py`：七種新增策略及五年固定 TP/SL 回測程式。
- `src/five_year_multi_market_kelly.py`：共用行情下載、技術指標、成本及風險統計程式。
- `results/complete_ranking_9556.csv.gz`：原策略、複合策略、固定盈虧策略與新增策略合併排名（Gzip 壓縮 CSV，解壓後可用試算表開啟）。
- `results/complete_ranking_9556.csv.gz` 可用 `gzip -dk complete_ranking_9556.csv.gz` 解壓；如在手機上，可用支援 Gzip 的檔案 App 解壓後匯入試算表。
- `results/overall_top50.csv`：總排名前 50 名。
- `results/positive_oos_over50.csv.gz`：五年及 OOS 都正收益且超過 50 筆交易的結果（壓縮 CSV）。
- `results/additional_strategy_results_728.csv.gz`：新增 728 組結果（壓縮 CSV）。
- `results/additional_strategy_top50.csv`：新增策略收益前 50 名。
- `results/additional_positive_oos_over20.csv`：新增策略中五年及 OOS 都正收益且超過 20 筆交易的結果。

## 執行

需要 Python 3.10+、`numpy`、`pandas` 及網路連線。從此資料夾執行：

```bash
python -m pip install -r requirements.txt
python src/run_strategies.py
```

首次執行會下載行情並建立 `src/five_year_market_data/` 快取；輸出 CSV 會建立在 `src/`。

## 研究限制

這是歷史研究程式，不會下單，也不保證未來收益。TP 是從 IS 選出，存在參數選擇偏差；各組交易數有限，OOS 期間不少組別成交筆數很少。全凱利倉位可能放大收益和虧損。CSV 排名是探索結果，應再做更嚴格的 walk-forward、合約規格核對與實盤模擬後再作判斷。
