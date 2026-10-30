# Trade Test 五年 9 市場 × 17 週期 × 原始 Python 策略碼去重稽核

更新：2026-10-31；本文件按本分支實際 Python 原始碼及現有 Git 去重清單計算，不代表新增五年 K 線回測已跑完。

## 目標範圍

- 真實五年：UTC 2021-10-10 00:00 至 2026-10-10 00:00（尾端不包含）。
- 市場（9）：BTCUSDT、ETHUSDT、SOLUSDT、GC=F、SI=F、ES=F、NQ=F、^TWII、USDJPY=X。
- 時區（17）：1m、2m、3m、5m、10m、15m、20m、30m、45m、1h、2h、3h、4h、6h、8h、12h、1d。
- 市場×時區：**9×17 = 153**；程式批次：**153×4 種執行分類 = 612**。
- 若「舊31種＋新7種」均為獨立策略且全部市場/時區適用，理論目標 **9×17×38 = 5,814 個市場×時區×策略**；這不是目前有程式實現或有五年資料的組合數。

## 實際 Python 原始策略碼（不可把四大執行分類誤稱 38 個不同策略）

| 執行分類 | 原始碼策略數 | 策略列表 |
|---|---:|---|
| original | 8 | Donchian20_10、MACD12_26_9、RSI14_EMA200、EMA50_200、Supertrend10_3、Bollinger20_2、RSI2_EMA200、Volume_Donchian20 |
| compound | 8 | EMA200+RSI14_pullback、EMA200+RSI2_mean_reversion、Donchian20+MACD、MACD+RSI50、Supertrend+EMA200、Supertrend+RSI50、WEMA20_50+Donchian20、WEMA20_50+MACD |
| fixed | 9 | EMA200+RSI14_pullback、EMA200+RSI2_extreme、EMA200+MACD_cross、Donchian20+ADX14、Bollinger20+RSI14_reentry、Supertrend+EMA200_flip、WEMA20_50+DailyMACD、WEMA20_50+DailyDonchian20、Stoch14+EMA200 |
| new | 7 | Turtle55_20_EMA200、Supertrend_ADX20、EMA20_50_ADX20、Keltner20_1.5ATR_EMA200、BB_Reentry_RSI_ADX25、Donchian20_Volume_EMA200、MACD_EMA200_ADX20 |

現有 `tools/run_legacy_all_timeframes.py` 實際會執行 **25 個舊策略定義槽 + 7 個新策略定義槽 = 32 種分類內策略任務**。但 `EMA200+RSI14_pullback` 同時在 compound 和 fixed，故舊策略只有 **24 個不重名訊號名稱**、加上新策略是 **31 個不重名訊號名稱**。按目前程式碼可明確排程的策略×市場×時區任務上限為 **4896**，尚未扣除資料/品種不適用。

**重要程式對帳缺口**：使用者要求舊31＋新7，但現有 runner 只掛了舊 25 個分類內策略定義（24 個不同舊名稱），非31個不同舊策略。`local_python_38_families_20261030.csv` 雖有 31 個標「舊」+7 個「新」的家族榜列，裡面有 **7 個新策略名稱被標成「舊」**：EMA20_50_ADX20、Keltner20_1.5ATR_EMA200、Donchian20_Volume_EMA200、Supertrend_ADX20、Turtle55_20_EMA200、MACD_EMA200_ADX20、BB_Reentry_RSI_ADX25。**該 38 列排行不是 38 個獨立、互不重複的已實裝策略定義**。需對帳找回真實舊策略代碼、確認規則，禁止靠複製或改名七種新策略冒充舊策略，亦不得把同一策略重跑作新完成。

## 612 批次去重現況（執行分類 × 市場 × 週期）

| 市場 | SHA+逐筆驗算完成：略過 | 既有摘要／日線快照：僅待核來源，不盲目重跑 | 待跑／已有隊列 | 失敗需修復後再跑 | 無核實五年分鐘線：不可捏造 |
|---|---:|---:|---:|---:|---:|
| BTCUSDT | 36 | 12 | 20 | 0 | 0 |
| ETHUSDT | 48 | 0 | 20 | 0 | 0 |
| SOLUSDT | 24 | 0 | 20 | 24 | 0 |
| GC=F | 4 | 0 | 0 | 0 | 64 |
| SI=F | 4 | 0 | 0 | 0 | 64 |
| ES=F | 4 | 0 | 0 | 0 | 64 |
| NQ=F | 4 | 0 | 0 | 0 | 64 |
| ^TWII | 0 | 3 | 0 | 1 | 64 |
| USDJPY=X | 0 | 3 | 0 | 1 | 64 |

合計：**124** 個完整逐筆驗算、**18** 個既有待稽核摘要／日線快照、**60** 個待/排隊、**26** 個失敗需修復、**384** 個缺五年真實分鐘資料，總數 **612**。其中完整逐筆驗算僅能獨立證明已保存的成交紀錄與績效重算一致，**不是在這段 ChatGPT 中重新計算五年行情的策略進出場訊號**。

- 已驗證批次全部 `SKIP_RETEST`；舊策略日線 `1d` 已有歷史結果者不重新測策略，較舊且無 SHA 的部分標示來源待核，不冒稱完整驗收。
- BTC 新策略12週期已有 Git 結果；按 SHA 及來源確認，不因缺少本地成交工件便直接重測。
- 衍生時區 2m／10m／20m／45m／3h 必須用**時間連續、來源核實的原始較小週期 OHLCV** 經程式嚴格重採樣，不能補造 K 棒。
- SOL 已有完成與失敗混合結果；只修正失敗來源並跑缺的週期，已完成批次不重算。
- 黃金、白銀、ES、NQ 等五年分鐘真實 OHLCV 尚未在當前工具中驗證；USDJPY 原 Yahoo 高低價異常，^TWII 休市日期不可補假 K，不能將無來源的組合標「成功」。
- 本 ChatGPT Python 容器目前已取回多個 Git 回測 ZIP，但裏面只有 `manifest.json`、`ranking.csv`、`trades.csv`、`checkpoint.json`，**沒有可供完整五年訊號重跑的 OHLCV 檔案**；故不能宣稱這輪已重跑缺漏策略。

詳細逐格 612 筆及來源：[`five_year_deduplicated_worklist_17timeframes.csv`](five_year_deduplicated_worklist_17timeframes.csv)。原策略執行入口：[`tools/run_legacy_all_timeframes.py`](../../tools/run_legacy_all_timeframes.py)。
