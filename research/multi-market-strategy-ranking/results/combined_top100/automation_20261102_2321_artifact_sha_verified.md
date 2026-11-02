# Trade Test 增量驗收｜2026-11-02 23:21 +08:00

## 本輪真正新增
- 五年真實 OHLCV 策略訊號：**0 組**；舊交易重播：**0 組**。
- **首次本輪實體 SHA256 驗證通過：BTCUSDT 1m compound 的 ranking.csv 與 trades.csv，共 2 份。**
- 由 GitHub Actions Run #41064675326 下載 artifact ID **12989801317**，ZIP 大小 16,555,494 bytes，實際 ZIP SHA256 **f7389fdbf4f194e3611cc79d23b19357f5f8985d40fc603f1bfeedf94380b472**，與 GitHub digest 一致。
- ZIP manifest.json: status=complete, family=compound, strategy_count=8, timeframe=1m, 2021-10-10 至 2026-10-10（終點不含），2,629,440 根 K 線，missing_or_irregular_intervals=0，**但 OHLCV 原始檔尚未獨立驗 SHA**。
- ranking.csv：32 筆資料列，實體 SHA256 **182cfd26ee03c9cb392bc2a617c968fda5c09a9a69f751d1a9e2db8706baaccc**，與 manifest 相同。
- trades.csv：924,586 筆資料列，實體 SHA256 **42552850f17bd33ef91739da3ad1c0688ef1a560516851558860d9b2a8c49579**，與 manifest 相同。
- manifest 每個 compound 策略宣告 tested_exit_count=9，但 saved_exit_count=1；**不可將 72 個宣告測試出場都視為有完整逐筆成交證據**。checkpoint.json 為 partial，manifest.json 為 complete，需保留兩者差異。
- Run #41066783962 的 SOLUSDT 1m artifact ID **12984099261** 亦已下載；ZIP SHA256 **10288265d25060207e153a6a270904cf15ef592cf74a081f8c47574ec2c581b7** 與 GitHub digest 一致，但 ZIP 內只有 138 bytes 的 tar.gz，內含空目錄 multi_SOLUSDT_1m_original；**沒有五年回測成果，不得列 complete**。
- 兩個 Run 的 artifact metadata 已查：#41064675326 37 件、#41066783962 31 件；BTC 1m original artifact ID 12990135479，ETH 1m/3m/5m artifact ID 12993586056/12988929734/12986299665，均存在且未過期，**未驗實體 CSV SHA**。
- 本輪未重跑舊策略 1d，未交 Jules、未新增 workflow、未動 main。

## 仍缺驗收
- BTC 1m original 與 ETH 1m/3m/5m ZIP 內 manifest、ranking、trades 實體 SHA 尚未驗證。
- 全市場 market×timeframe×family×strategy×exit 去重 completed/required 尚未核定；無法把 artifact 存在當作完整五年訊號。
- SOL 真實 Binance daily ZIP 修補、完整 Python runner 編譯及五年端對端回測尚未驗證。
- 全 38 策略榜與 Kelly Top100 **保留原版，不以本輪有限證據覆寫**。

## 排行榜（既有、未重新驗證）
- [38 家族榜](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)

下一輪應優先取回 BTC 1m original、ETH 1m/3m/5m ZIP，核對逐檔 SHA 與策略/出場唯一鍵，再處理 SOL 真實資料。
