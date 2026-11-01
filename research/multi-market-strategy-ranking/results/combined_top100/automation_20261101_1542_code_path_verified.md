# Trade Test 2026-11-01 15:42 +08:00 — 程式路徑修復與增量驗收

## 本輪已核實

- 使用 GitHub connector 讀取隔離分支 `report/trade-test-multi-market-20261030` 的 research 遞迴樹（311 entries），定位真實 Python 主程式為 `research/multi-market-strategy-ranking/tools/run_legacy_all_timeframes.py`，blob SHA `3809a45ccebd245d1244f05fa2056710db9d6278`。先前嘗試根目錄 `tools/run_legacy_all_timeframes.py` 得到 404，原因是**路徑錯誤**，不是程式不存在。
- 直接讀取主程式：`DERIVED["20m"] = ("5m", 4)`；`load_market_ohlcv` 檢查每組 4 根、五年窗口起迄、衍生週期連續性，未發現使用虛構缺口的明示邏輯。未以真實 OHLCV 實跑，不宣稱程式已通過行情測試。
- 查核既有 Actions Run 41066783962 的 artifact 列表：31 份；ETH 1m id 12993586056（151493344 bytes）、3m id 12988929734（49106611 bytes）、5m id 12986299665（28902635 bytes），均未過期。**僅核對遠端清單，未下載、未獨立驗 SHA**。
- 既有狀態文件 `TRADE_TEST_CURRENT_STATE_20261101.md` 記載 188 個已存交易重播分類批次與 424 個缺口；分類批次不是逐策略出場配置，不能用來宣稱 38 策略完成率。

## 本輪新實測與驗收統計

- 新執行五年真實 OHLCV 策略訊號：**0 個配置**。
- 新增舊交易回放：**0**。
- 新增內層 CSV/行情 SHA256 獨立驗證：**0**。
- 本輪修復：**主程式位置已定位並直接讀取**，排除先前錯誤的根目錄 404 阻礙。
- 完整完成數（market×timeframe×family×strategy×exit）：**尚不能由目前的分類清單可信計算**；不可填造 completed/required。

## 下一個可執行工作

1. 優先下載並驗證 ETH 1m/3m/5m 已保存工件的內層 manifest、排名、逐筆交易 SHA，按完整唯一鍵去重，勿重跑已完成配置。
2. 取得真實連續五年 5m OHLCV 並驗證原始來源 SHA，才補測缺失 20m。非加密五年分鐘資料不可得時記 unavailable。
3. 舊策略全部九市場 1d 一律保留歷史基準，不重跑；不交 Jules，不新增 workflow，不動 main。

既有榜：
- [38 家族歷史榜](local_python_38_families_20261030.csv)
- [Kelly Top100 歷史榜](local_python_kelly_top100_20261030.csv)

兩榜均未因本輪檢查升級為完整驗收。
