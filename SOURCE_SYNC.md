# 17 — Donchian20+ADX14

同步日期：2026-11-25（台灣時間）。本次復原既有策略來源，沒有新增策略或調整參數。

- `strategy.py`：逐字複製本機 `C:/Users/User/trade-test/research/multi-market-strategy-ranking/src/five_year_low_drawdown_fixed_rr.py`；包含本策略及該來源共用的策略規則，並非只產生 EMA 訊號的佔位檔。
- 同目錄 Python 模組及 `research/multi-market-strategy-ranking/src/`：本機原始共用依賴。
- `strategy.pine`：逐字複製 `C:/Users/User/trade-test/research/multi-market-strategy-ranking/pine/donchian20_adx14.pine`。
- 首頁代表商品／週期：BTCUSDT / 6h；原始 Python 多週期入口為 `research/multi-market-strategy-ranking/tools/run_legacy_all_timeframes.py --symbol BTCUSDT --timeframe 6h --family fixed`。原入口依 family 執行多個既有策略，沒有單策略選項；由輸出篩選 `Donchian20+ADX14`。

## 驗證與限制

Python 策略引擎與共用出場程式已通過語法編譯檢查。本次沒有重跑五年行情或 TradingView。Pine 來源照原檔保存，預設商品、週期、風控和首頁最佳配置可能不同，不能宣稱績效相同。

本機最新版 `src/run_intraday.py` 第 227 行有未結束字串，不能作為可執行版本發布；本次保留分支原有的該依賴版本，不覆蓋為這份損壞檔。因此完整多週期資料取得流程尚未驗證，不能把本次原碼復原標成回測通過。

Python strategy.py Git blob: `e106b7c726b90a64ecd870416b7a533c45a73327`
Pine strategy.pine Git blob: `79f86734aec038c50719ad86ae149f33919e895e`
