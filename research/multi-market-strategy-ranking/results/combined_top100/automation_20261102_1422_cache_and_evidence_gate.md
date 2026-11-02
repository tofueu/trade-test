# Trade Test — 2026-11-02 14:22 +08:00 — 原始程式與證據門檻核查

## 本輪可重現實測
讀取已保存的 `trade_test_20261102_1135_sha_audit.json`，以 Python json / collections 重新計算：13 records；BTCUSDT 1m compound 1 筆 family×timeframe；ETHUSDT 1m/3m/5m 各 4 筆；tested_exits - saved_exits = 448；所有 26 個 checks 內的 `sha_ok` 欄位均為 true。**這是先前驗證結果的欄位重算，並非本輪重新計算 26 個實體 CSV SHA256，也不是交易回放。**

重要的新證據限制：此 JSON 每筆只有 `artifact,symbol,timeframe,family,strategy_count,tested_exits,saved_exits,checks`，沒有個別 strategy ID、exit ID、每一個 variant 的唯一鍵、逐筆交易來源或 OHLCV SHA。故**不能從此 JSON 推導 448 個具體缺失的策略出場唯一鍵**；不能把 448 當成新增回測待跑數，也不能由 `sha_ok` 宣稱已獨立驗證行情。

## 原始程式核對（指定隔離分支）
`research/multi-market-strategy-ranking/src/run_intraday.py` 的 `load_real_ohlcv` 目前：
1. 先檢查 five-year 首尾覆蓋，若缺起點或末端，會在任何 daily ZIP 修補前失敗。
2. 先檢查 warm-up 完整性，若 warm-up 缺失，亦在修補前失敗。
3. 對五年窗口內的內部缺口，只在 `if gaps and not cache_hit:` 時嘗試 daily archive 修補。因此快取已有缺口時會直接拒絕，而非進入驗證修補。
4. `restore_gap_klines_from_binance_daily_archive` 只掃描窗口內部相鄰 K 線之間的缺口，無法修補窗口首尾與 warm-up 缺口。其每日 ZIP SHA receipt 是資料來源證據，但不等於整段五年 K 線已重新獨立驗證。
5. 同一 runner 的 CLI `--symbol` choices 僅 `BTCUSDT`，但 `load_real_ohlcv` 支援 BTC/ETH/SOL；不能假設此 CLI 可直接執行 SOL。

上述是程式碼靜態核對，**不是 SOL 當次失敗根因已實證**。下一次程式修補應先建立缺口分類（起點/末端、warm-up、內部、cache），對真實 Binance daily ZIP 完成 SHA、時間戳、OHLCV、無衝突去重檢查後才原子寫回；修補後需重新驗證五年與 warm-up 完整性。不能 forward-fill 或插值。需保留既有有效 cache 和 checkpoint，不覆蓋已驗證成果。

## 增量回測及排名
- 本輪新跑出五年真實 OHLCV 策略訊號：**0**。
- 本輪舊交易紀錄回放：**0**。
- 本輪獨立重算實體工件 SHA：**0**。
- 本輪 Python 實際重算：**13 筆既有 JSON 稽核記錄的分組與 448 差額**。
- 全 9 市場 × 17 指定時區 × 38 策略 × 出場方式的 completed/required：**尚未核定**；缺五年真實 OHLCV 的非加密時區應標 unavailable，不得補造。
- 兩份排行榜未覆寫，不能把舊交易重播計為新增五年策略訊號。
- 所有九市場舊 31 策略 × 1d **禁止重跑**；新策略 1d 僅去重後補缺。
- 未交 Jules 1/2；未新增 workflow；未改 main。

[38 策略家族既有榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)

[既有 Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
