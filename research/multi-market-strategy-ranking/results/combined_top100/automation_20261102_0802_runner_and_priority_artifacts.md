# Trade Test 2026-11-02 08:02 +08:00 — 原始 runner 定位及 Actions 工件收取索引

## 本輪可查證的新發現
已從隔離分支直接讀到正確 Python runner：`research/multi-market-strategy-ranking/src/run_intraday.py`。先前查詢 `src/run_intraday.py` 的 404 是漏掉 repository 子目錄，不代表原始碼不存在。

已向 GitHub Actions API 重新讀取兩個指定 run 的工件清單（僅第一頁，故不能當作全量）：
- Run 41064675326：BTC 1m original artifact ID 12990135479，112080486 bytes，GitHub digest sha256:54324a419f95bbd31c4da3dd2ab50c800334e4cb587033ba3339ad637e5a98bc；BTC 1m compound ID 12989801317，16555494 bytes，sha256:f7389fdbf4f194e3611cc79d23b19357f5f8985d40fc603f1bfeedf94380b472。兩者均顯示 expired=false。
- Run 41066783962：ETH 1m ID 12993586056，151493344 bytes，sha256:507ac6862784d2ea73dafa04b76d7aca86b984ee49b61f39128ea78d80885f31；ETH 3m ID 12988929734，49106611 bytes，sha256:a53868d60ad92fb3711f66da0b446ea3a2a2f03b4b3eb55954533d2185cb34a1；ETH 5m ID 12986299665，28902635 bytes，sha256:2039fd39c0b82ce4da8a2aa4f94cf9e800f02d6ea9930adf2b924d40f7f27ae6。三者均顯示 expired=false。

以上為 GitHub 回報的 digest，**本輪尚未下載 ZIP 位元組自行計算 SHA256**；也尚未檢查其內部 manifest、交易 CSV、行情 SHA，故僅列為「工件存在／SHA 待獨立驗證」，不列 complete。

## 程式修復定位
`run_intraday.py` 的 `load_real_ohlcv` 中，缺口修補條件為 `if gaps and not cache_hit:`。因此已有不完整快取時會跳過 daily archive 修補，最終拋出 Irregular or missing five-year candles。另 warm-up 完整性驗證發生在缺口修補之前；即使後續可以從交易所補到真實資料，warm-up 缺口仍會提前拒絕。本輪已確認此程式路徑，**尚未修改程式或證明 SOL 4h 當次是 cache_hit**。修復須維持失敗即拒絕、每日 ZIP SHA 收據、原子更新快取，並使用真實 Binance 行情驗證。

## 完成口徑與本輪新增
- 新跑出五年真實 OHLCV 策略訊號：**0 組**。
- 舊交易回放驗算：**0 組**。
- 本輪自行驗證工件 ZIP SHA：**0 份**。
- 新增可定位優先收取工件：**5 份**（BTC 2、ETH 3）。
- completed/required：**尚未核定**。須先合併 Git manifest、完整交易明細與 Actions 工件的唯一鍵 `market×timeframe×family×strategy×exit`，按證據層級去重。
- 舊31策略×9市場×1d 禁止重跑；本輪未執行。
- 非加密五年分鐘資料不可用須標 unavailable，不得合成。
- 38 家族歷史榜、Kelly Top100 尚未重算，不能視為完成五年驗收或伯努利 iid 已證明。
- 未交 Jules、未新增 workflow、未動 main。

下一步：下載上列 5 個未過期工件並驗證 ZIP digest、manifest、交易 CSV 及 OHLCV SHA；再以已驗完成唯一鍵排除重跑，對 SOL 缺口做真實 Binance daily archive 修復測試，最後才執行缺失的 Python 策略配置。

[38 家族歷史榜](local_python_38_families_20261030.csv) | [Kelly Top100 歷史榜](local_python_kelly_top100_20261030.csv)
