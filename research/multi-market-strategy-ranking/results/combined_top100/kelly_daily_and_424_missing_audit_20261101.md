# 五年回測增量驗收：日線 Kelly 公式與 424 缺口 — 2026-11-01

這輪直接在 ChatGPT 本地 Python 實際執行 `/mnt/data/trade_test_daily_kelly_check.py`，處理已留存的 13 份日線 ZIP，解包其中 36 份分類排名工件（部分來源重複，同一 symbol+family 去重後 31 類），合計掃描 3,460 行配置。與之前只重算交易收益不同，本次獨立驗算樣本內 Kelly 公式。

- 依據 `IS勝率_p`, `IS失敗率_q`, `IS平均贏虧比_b` 重算 `max(0,100*(p-q/b))`；資料未提供贏虧比或 IS 勝敗統計者依原始回測約定以 Kelly 0 處理，不編造勝率或盈虧比。
- 檢查 3,460 行，**Kelly 算式不符 0 行**；Kelly 類型配置的 `實際風險_pct` 超過該筆 `IS_Kelly_pct` **0 行**。**1,364 行 Kelly 為 0**（包含部分重複工件）。
- 注意 `固定1R` 配置不受此處「Kelly 類型配置」上限檢查約束，不能因此宣稱全部固定1R策略都符合使用者要求的 Kelly 風險限制。未獨立重建 IS 逐筆樣本，也未重算完整 OOS、最大回撤。
- Python 明細在會話容器 `/mnt/data/TradeTest_daily_Kelly_audit_20261101.csv`；該 CSV 尚未上傳本 Git 分支。
- Python 使用現有 188 批去重完成清單 `/mnt/data/TradeTest_incremental_BTC1m_merged_20261031.csv`，對 9 市場×17 時區×4 family=612 分類組合重新展開，**188 個已有真實交易紀錄與獨立五年收益回放，424 個尚無這個層級的本地驗收證據**。逐筆缺口 CSV 在會話容器 `/mnt/data/TradeTest_424_missing_batches_20261101.csv`，本 Git 報告沒有假稱已上傳此 CSV。
- 424 缺口分布：BTCUSDT 28、ETHUSDT 4、SOLUSDT 4、GC=F 64、SI=F 64、ES=F 64、NQ=F 64、^TWII 64、USDJPY=X 68。缺口中 **384 個是非加密六市場的 16 種日內時區×4類**，目前沒有可查證五年 OHLCV 來源與合格工件，**不是測試失敗後能填數字的組合**。BTC/ETH/SOL 的 20m 也尚未補驗；USDJPY 日線四類仍未驗。
- 本輪實測 Python 對 `data.binance.vision` 與 `raw.githubusercontent.com` 的 DNS 均回傳 `[Errno -3] Temporary failure in name resolution`，無法在此 Python 環境直接下載缺漏原始行情。已保存工件可繼續檢查，但不能冒充未執行之 OHLCV 訊號回測。
- 原始 31 舊+7 新策略實作覆蓋仍需另行補齊。此驗收只涵蓋原先已實作策略配置，沒有完成所有要求。**保留 partial，絕不標記全數完成。** 不交 Jules、不動 main、不建立 workflow。

