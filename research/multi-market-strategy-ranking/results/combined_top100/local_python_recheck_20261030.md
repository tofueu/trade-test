# Trade Test 五年 Python 增量驗證進度（臺灣時間 2026-10-31）

## 必守規則

- **完整五年**：交易回測窗口 `2021-10-10 00:00 UTC` 至 `2026-10-10 00:00 UTC`（結束時間不含），2026-10-09 為最後交易日。不是一年樣本。
- **僅指定市場**：BTCUSDT、ETHUSDT、SOLUSDT、黃金 GC=F、白銀 SI=F、美國指數 ES=F 與 NQ=F、臺灣指數 ^TWII、USDJPY=X。
- **僅指定時區**：1m、2m、3m、5m、10m、15m、20m、30m、45m、1h、2h、3h、4h、6h、8h、12h、1d。**排除**之前誤列的秒線、週線、月線；153 個商品×週期組合，612 個（×original/compound/fixed/new）分類狀態欄位。這是待驗證矩陣，非已完成數。
- **不可重跑**：先查 Git `results/all_timeframes/*/manifest.json`、已保存歷史日線基準、既有 GH Actions artifacts，再比對 `ranking.csv`、`trades.csv` SHA256、行情 SHA256 與交易配置。舊策略 1d 已跑過，無論何時都不應再重跑；沒有單項 SHA 的舊日線快照先標記待核實，不能當作已全面驗證。
- **不得交 Jules、不新增 GitHub workflows、不修改 main**。所有更新只在既有隔離分支。

## 此次已真正用本機 Python 新驗的成交資料

- 原累計：90 批、9,328 配置；此次新增 BTCUSDT `1m compound`（32配置，924,586逐筆成交），ETHUSDT `3m` 的 `original`（288配置，1,954,098逐筆成交）、`compound`（32配置，298,410成交）、`fixed`（36配置，228,550成交）、`new`（28配置，107,844成交）。
- **目前總計 95 批、9,744 個配置，收益、交易數、前四年 IS Kelly、五年最大回撤重算不一致數 0**；本次新增 5 批、416 配置。已以 300 組隨機序列對照原始參考算法驗證高速逐筆權益計算函式；所有新增批次的 `manifest` 完整且 `ranking.csv` 與 `trades.csv` SHA256 正確。
- **38 個策略家族**保留。收益 Top100 仍有 72 筆本機逐筆驗算、28 筆僅原 Git 歷史快照（已標註，不能混淆）；本次新增未改變榜首。
- 從先前誤算 225 對修正為 **153 對**；其中 **27 對**有本機實際逐筆交易紀錄，**15 對**涵蓋四分類；不能認定其餘為已完成。
- **重要分別**：上述本機 Python 重算的是既有完整五年實際成交紀錄與 Kelly/回撤，**不是**在當前容器中重新取得完整原始五年 OHLCV 後重新生成所有策略訊號。原始行情不在此聊天工作環境、直接連接下載源受阻。

## Git 已完成／已產出而不要重跑的部分

- 已檢查 Git tree，至少 **30 個原有 `results/all_timeframes` manifest** 已在此分支保存（含 BTC 1d 舊三分類、BTC 4h 舊三分類，ETH 1d/4h 四分類，以及黃金、白銀、美國 ES/NQ 1d 四分類）。其中各個資料須維持原 `sha256`。
- 已檢查舊 BTC run `41064675326`：**36 個** 1m~1d 舊分類結果工件存在，原 run 的整體 `failure` 不等於工件都失敗。新近到達的 BTC 1m original/compound 必須先驗 SHA，不可重跑。
- 已檢查多市場 run `41066783962`：ETH 1m/3m/5m 有大容量結果工件；SOL、^TWII、USDJPY部分只有約 300-byte 的失敗工件，**不能當作回測完成**。新跑中的 job 若只是已存在結果，不可再重複派工。
- 舊日線 9,556 行的既有基準保留；不得為了補其他小時區重新執行舊策略日線。
- 已修補 `run_legacy_all_timeframes.py` 漏列 `20m`：以四根**連續且原始驗證**的 5m K 線聚合，沿用原有嚴格 OHLCV gap 檢查（commit `5e87bbbf164cc1ffa17a9eaab6076a0539d44a75`）。

## 本輪 Git 成果與後續待查

- [指定17週期去重清單](five_year_deduplicated_worklist_17timeframes.csv)：每格列出已提交 Git、已有工件待驗 SHA、既有歷史日線免跑、正在既有 run 排隊、原始資料缺失、尚未執行等，不把 612 類別視為已測。
- `local_python_kelly_top100_20261030.csv`、`local_python_38_families_20261030.csv` 是既有兩份正式 Git 榜單；此輪不改變合格 Top100 排序，新增配置明細另以本機驗算檔保存。
- **待處理**：驗 BTC 1m original（大容量工件）、ETH 1m 及其餘已到達工件；檢查 SOL 僅用真實 Binance 每日 ZIP 修補月檔缺漏；^TWII 交易所休市不補假 K、USDJPY 異常高低價不篡改；其餘非加密商品五年分鐘資料在現有 Python 來源程式中尚無可驗證來源，不能捏造策略結果。
- 每六小時在既有 Git 分支與 ChatGPT 自動任務對話回報進度。六小時自動驗收只能在觸發時執行，不能誤稱聊天中的 Python 會在訊息結束後不間斷常駐。

## 未驗證與交付邊界

**全部測試仍未完成。** 不能把已保存成交紀錄的資金管理驗算當作所有 38 策略在所有市場、全部指定 17 時區重新跑完五年 OHLCV 訊號。缺五年真實資料標 `unavailable`；勝敗 Bernoulli iid 不能因 runs-test 未拒絕而聲稱證明；尚未完成 Pine/TradingView 逐筆 parity。
