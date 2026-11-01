# Trade Test 增量稽核｜2026-11-01 18:38 Asia/Taipei

## 本輪讀取與計算
直接從既有隔離分支取得兩份 CSV 全文，按 CSV 欄位重新統計，不以排行榜列數代表回測完成數。本輪計算由 GitHub connector 取得內容後使用 JavaScript 執行；未執行 Python 策略引擎、未取得新 OHLCV、未下載 ETH 大型 ZIP。

- Kelly Top100：100 列，逐 商品×週期×策略分類×策略×出場方式×倉位法 去重為 100 列；CSV blob SHA `ed2ee1cd40a9f4b6f3a17739f0ec66892998fc06`。
- Top100 週期分布：1m=0、2m=0、3m=0、5m=0、10m=0、15m=0、20m=0、30m=0、45m=0、1h=0、2h=4、3h=0、4h=15、6h=22、8h=34、12h=23、1d=2。**僅 6/17 個指定週期在 Top100 出現，不代表其餘 11 個週期未執行或績效不達標。**
- Top100 分類：original 68、compound 24、new 5、historical_old 2、fixed 1；這些是 CSV 分類值，不可視為舊31＋新7的策略家族完整覆蓋。
- Top100 來源：舊交易回放 `trade_fills_replayed_locally_sha256` 98 列；`complete_sha256_verified` 2 列，仍待原始行情獨立核對。
- 38 家族歷史榜：38 列，CSV blob SHA `c91e0ed0e43520ba972b50b188b1db8443d97ee1`；週期 1d=24、8h=2、2h=2、6h=3、4h=3、12h=4。榜單只取每家族代表配置，不能當成已跑週期覆蓋。
- GitHub Actions Run #41066783962：ETHUSDT 1m artifact 12993586056（151493344 bytes）、3m 12988929734（49106611 bytes）、5m 12986299665（28902635 bytes）均未過期；外層 digest 由 GitHub 宣告，**本輪沒有獨立下載重算 ZIP/CSV SHA**。

## 本輪實際新增與驗證層級
- 新跑五年真實 OHLCV 策略訊號組合：**0**
- 新增舊交易紀錄重播：**0**
- 新增內層 SHA256 驗證：**0**
- 新增 CSV 原始欄位覆蓋稽核：**2 份**
- completed/required（market×timeframe×family×strategy×exit）：**尚無可信分子/分母**；不能用 100 或 38 代替。
- iid 已證明：0（依既有稽核）；不宣稱已驗證。

## 待處理與禁止事項
優先取回 ETH 1m/3m/5m 與 BTC 1m original/compound 的既有 artifact，逐層核對 manifest、CSV、OHLCV SHA，按唯一鍵跳過已驗收組合。舊31策略×9市場×1d 絕對禁止重跑；新7策略 1d 只補有真實五年資料且未完成者。20m 僅允許四根連續真實5m K棒聚合，非加密市場五年分鐘資料缺失標 unavailable。不可交 Jules、不可新增 workflow、不可動 main。

## 既有榜
- [全部家族歷史榜](local_python_38_families_20261030.csv)
- [Kelly Top100 歷史榜](local_python_kelly_top100_20261030.csv)

本輪沒有產生新的可驗證策略績效，因此不更改既有排名。