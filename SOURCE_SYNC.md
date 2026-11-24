# 24 — EMA200+RSI14_pullback

同步日期：2026-11-25（台灣時間）。本次復原既有策略來源，沒有新增策略或調整參數。

- `strategy.py`：逐字複製本機 `C:/Users/User/trade-test/research/multi-market-strategy-ranking/src/five_year_compound_strategy_sweep.py`；包含本策略及該來源共用的策略規則，並非只產生 EMA 訊號的佔位檔。
- 同目錄 Python 模組及 `research/multi-market-strategy-ranking/src/`：本機原始共用依賴。
- `strategy.pine`：逐字複製 `C:/Users/User/trade-test/research/multi-market-strategy-ranking/pine/ema200_rsi14_pullback.pine`。
- 首頁代表商品／週期：SOLUSDT / 30m；原始 Python 多週期入口為 `research/multi-market-strategy-ranking/tools/run_legacy_all_timeframes.py --symbol SOLUSDT --timeframe 30m --family compound`。原入口依 family 執行多個既有策略，沒有單策略選項；由輸出篩選 `EMA200+RSI14_pullback`。

## 驗證與限制

Python 策略引擎與共用出場程式已通過語法編譯檢查。本次沒有重跑五年行情或 TradingView。Pine 來源照原檔保存，預設商品、週期、風控和首頁最佳配置可能不同，不能宣稱績效相同。

本機最新版 `src/run_intraday.py` 第 227 行有未結束字串，不能作為可執行版本發布；本次保留分支原有的該依賴版本，不覆蓋為這份損壞檔。因此完整多週期資料取得流程尚未驗證，不能把本次原碼復原標成回測通過。

Python strategy.py Git blob: `869cd24b461cbabd3b9a93879d9f5c5a9de93685`
Pine strategy.pine Git blob: `16b009f61b1d0f61659fe9beaea64be75ea2f974`
