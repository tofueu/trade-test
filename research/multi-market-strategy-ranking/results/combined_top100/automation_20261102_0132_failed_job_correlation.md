# 2026-11-02 01:32 +08:00 — 失敗工作與空工件交叉核對

來源：GitHub Actions Run 41066783962 的 jobs 與 artifacts API，當輪重新取得。

## 本輪新查證

- jobs API 第一頁 30 筆中，14 個失敗 job 均在第 6 步 `Execute four actual strategy families with genuine candles` 失敗。
- 這 14 個失敗 job 與 14 份約 287–297 bytes 的 artifact 逐市場／週期一一對應：SOLUSDT 的 1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d 共 12 份，另 ^TWII 1d、USDJPY=X 1d 各一份。
- SOLUSDT 3m artifact 12985660219 前輪已實際解包確認只有空目錄，沒有 manifest、ranking、trades；本輪沒有重新下載或重跑。
- 失敗步驟的實際 stderr 尚未取得，因此**不能斷言根因是缺少哪一天的 OHLCV**。小 ZIP 與失敗步驟的相關性已驗證，因果尚待日誌。
- 舊 31 策略全部市場 1d 一律保護，不可重跑。其餘已驗完整的配置亦不可重跑。不能把 14 個失敗 job 全數直接重跑。

## 進度分類

- 本輪新跑出五年 OHLCV 策略訊號：**0** 組。
- 本輪僅舊交易回放：**0** 組。
- 本輪新增 SHA256 驗證：**0** 份。
- 新增證據：14 個失敗 job 與 14 個極小 artifacts 的一對一關聯，以及失敗步驟定位。
- completed/required：**尚無可靠跨全部 manifest 的唯一鍵總表，不能填數字**。
- 38 家族榜、Kelly Top100：維持原版；不以舊交易回放或空工件增列完成數。

## 下一個可執行修復

1. 取得失敗 job 第 6 步 stderr／log，先鎖定資料讀取、缺口檢查或策略引擎的確切錯誤。
2. 只以 Binance 真實 daily archive 補 SOL 缺日；驗證連續 OHLCV 與 SHA 後，依 manifest 唯一鍵補跑缺失非 1d 配置。
3. ^TWII、USDJPY=X 1d 先查原始行情與失敗日誌；舊策略 1d 不重跑，新策略只補真正缺失者。
4. 優先保留 BTC 1m 與 ETH 1m/3m/5m 已驗證交易工件，不重算。

原始連結：https://github.com/tofueu/trade-test/actions/runs/41066783962
