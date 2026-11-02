# Trade Test — 2026-11-02 15:27 +08:00 — 快取缺口修補實際程式變更

## 本輪修改
在既有隔離分支直接修改 `src/run_intraday.py`（原始路徑含 `research/multi-market-strategy-ranking/`），提交 `417d2e191228504f249e3b3a94d3e3042cd330a6`。

1. 原本 `if gaps and not cache_hit` 改為 `if gaps`：即使五年 OHLCV 來自既有 CSV 快取，仍可透過既有 `restore_gap_klines_from_binance_daily_archive` 逐根取 Binance 真實 daily ZIP；函式會驗證缺失時間戳、OHLCV、重複衝突及 ZIP SHA，不得插值。
2. 新增 `gaps_repaired_from_cache`，僅當原快取有缺口且修補通過時，允許原子替換快取與來源 SHA receipt；失敗則不寫回。
3. CLI `--symbol` choices 加入 ETHUSDT、SOLUSDT，對齊載入函式既有白名單。

## 驗證與尚未修復的限制
已從 Git 再次讀取更新後檔案 blob `5c57e93a488def33a0b3c16e7a917a4f3c27934a`，以程式文字斷言確認上述修補分支、SHA receipt 寫入、CLI choices 都存在。**尚未執行 Python 語法編譯、真實 SOL Binance daily archive 下載、五年 K 線連續性驗證或策略回測。** 不得將靜態斷言稱為運行測試。

原有程式仍在 daily ZIP 修補之前檢查五年首尾及 warm-up 完整性，故起點、終點或 warm-up 缺失仍會提前拒絕；本次僅修復「快取存在且窗口內部有缺口」路徑。原本快取 SHA receipt 不吻合時仍拒絕修補，以免信任遭篡改資料。下次需做真實資料測試，補首尾/warm-up 的安全修補，再驗證所有 5 年 K 線與 SHA。

## 本輪成果與去重
- 新跑出五年真實 OHLCV 策略訊號：**0 組**。
- 僅舊交易紀錄回放：**0 組**。
- 本輪實體 CSV SHA256 重新驗算：**0 份**。
- 本輪程式修復：**1 檔（兩個功能點及快取原子寫入條件）**；靜態核對通過，未完成運行驗證。
- 前輪 13 份工件稽核摘要：744 個宣告已測出場、296 個宣告已保存、448 個尚缺保存證據；這 448 個不能直接認定為未執行訊號，亦不可整批重跑。
- 九市場 × 17 時區 × 38 策略 × 出場方式的 completed/required：**尚未可靠核定**。
- BTC 1m original/compound、ETH 1m/3m/5m 已有前輪 SHA 驗證證據；本輪不重跑。
- 舊 31 種策略的九市場 1d **禁止重跑**；非加密五年分鐘資料不可得時列 unavailable。
- 未交 Jules、未新增 workflow、未修改 main。

[38 家族既有排行榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)

[既有 Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
