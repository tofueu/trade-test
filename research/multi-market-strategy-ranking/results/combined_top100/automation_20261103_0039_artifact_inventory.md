# Trade Test 2026-11-03 00:39 +08:00｜GitHub artifact 增量盤點

## 本輪實際核查
透過 GitHub API 重新查詢既有 Run 41064675326（37 件）及 Run 41066783962（31 件），共 68 件 artifact，均回傳 expired=false，預定 2026-11-29 到期。此處是 GitHub artifact **中繼資料及服務端 ZIP digest** 的盤點，**不是**本輪下載 ZIP 的 SHA256 實測，更不是 CSV / OHLCV SHA 驗證或新策略回測。不得用 68 件換算 completed 配置。

| 優先項目 | artifact ID | ZIP bytes | GitHub 宣告 ZIP SHA256 | 驗收狀態 |
|---|---:|---:|---|---|
| BTC 1m original | 12990135479 | 112080486 | 54324a419f95bbd31c4da3dd2ab50c800334e4cb587033ba3339ad637e5a98bc | 已存在、此輪未驗檔 |
| BTC 1m compound | 12989801317 | 16555494 | f7389fdbf4f194e3611cc79d23b19357f5f8985d40fc603f1bfeedf94380b472 | 前輪曾驗 CSV；本輪未重驗 |
| ETH 1m | 12993586056 | 151493344 | 507ac6862784d2ea73dafa04b76d7aca86b984ee49b61f39128ea78d80885f31 | 已存在、此輪未驗檔 |
| ETH 3m | 12988929734 | 49106611 | a53868d60ad92fb3711f66da0b446ea3a2a2f03b4b3eb55954533d2185cb34a1 | 已存在、此輪未驗檔 |
| ETH 5m | 12986299665 | 28902635 | 2039fd39c0b82ce4da8a2aa4f94cf9e800f02d6ea9930adf2b924d40f7f27ae6 | 已存在、此輪未驗檔 |

來源：
- https://github.com/tofueu/trade-test/actions/runs/41064675326
- https://github.com/tofueu/trade-test/actions/runs/41066783962

## 額外發現
Run 41066783962 中 SOL 1m/3m/5m/15m/30m/1h/2h/4h/6h/8h/12h/1d 工件 ZIP 只有 293–297 bytes；與正常交易明細大小顯著不同，列為疑似空工件，須解壓檢查，不能視為完成，也不能在未驗證原始資料前重跑。^TWII 1d 與 USDJPY=X 1d 也僅 287、296 bytes；這是本次發現的待驗證工件，**不是**行情 unavailable 的證明。

## 本輪計數
- 新增五年真實 OHLCV 策略訊號：0
- 舊交易回放：0
- 新增本地獨立 SHA256：0
- GitHub 工件中繼資料重新核查：68
- 新增排行榜項目：0；保留原兩榜
- 全市場 completed / required：未核定，待 manifest + CSV + SHA + 唯一鍵逐配置盤點

## 既有榜單
- [38 策略家族](./local_python_38_families_20261030.csv)
- [Kelly Top100](./local_python_kelly_top100_20261030.csv)

## 下一個可執行工作
優先下載 BTC original、ETH 1m/3m/5m ZIP；以 Python 比對下載 ZIP SHA、內部 manifest(status=complete)、ranking/trades SHA、原始 OHLCV 來源與完整五年時間窗，逐一產生 market×timeframe×family×exit 唯一鍵。SOL 需先修補並核對真實 Binance daily archive；舊31策略九市場 1d 嚴禁重跑。不得把既有交易 CSV 回放算成新策略訊號。禁止 Jules、新 workflow、main 修改。
