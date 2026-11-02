# Trade Test — 2026-11-02 17:29 +08:00

## 本輪程式修復（實際提交）
- 修正 `src/run_intraday.py` 內部缺口稽核只檢查 `START..END`、卻在修補前拒絕 warm-up 內部缺口的矛盾。
- 改以 `warm_start..END` 的全部相鄰 K 線時間戳偵測缺口，並讓既有 Binance daily ZIP 實證修補函式處理 warm-up 內部缺口；修補後才驗 warm-up 連續性與五年完整覆蓋。
- 原始程式提交：`34b6c6c8757643918e5cf4128ea8d2771e87381a`。
- 已用 Python pandas 獨立單元情境測試：模擬 5m warm-up 中缺一根，確認新稽核區間能發現缺口、補入同時間戳後連續性成立。**此測試使用合成時間戳，並非行情或策略回測；絕不列入完成數。**
- 本地直接取得私有 GitHub raw 程式失敗（連線 DNS/網路錯誤），因此尚未對整份 runner 執行 `py_compile` 或真實 SOL Binance ZIP 端對端測試；不得聲稱修復已經整體驗收通過。

## 本輪完成口徑
- 新增五年真實 OHLCV 策略訊號：**0 組**。
- 僅舊交易紀錄驗算：**0 組**。
- 新增真實來源 SHA 驗證：**0 份**。
- 已存工件與 SHA 的前輪證據保留，沒有重跑任何既有配置；舊策略九市場 1d 一律不重跑。
- `completed/required` 尚無可核定的全市場唯一鍵清單，故不造數字。
- SOL 修復尚未取得五年完整真實 OHLCV；不能列 completed。
- 448 個未宣告保存出場結果不能當作 448 個新策略回測。
- 不交 Jules 1/2，不新增 workflows，不動 main。

## 後續必要驗收
1. 取得修復後原始 runner 的可執行副本，`python -m py_compile`，執行真實 SOL daily archive 缺口復原並比對原始 K 線 SHA。
2. 從 Git manifest、ranking、trades 與 Actions artifacts 逐一建立 market×timeframe×family×strategy×exit 唯一鍵，區分已存未驗 SHA／已驗交易／完整五年訊號。
3. 只對缺失且具有真實五年資料的配置執行策略，更新 38 家族榜及合格 Kelly Top100。

[38 家族既有排行榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)

[Kelly Top100 既有排行榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
