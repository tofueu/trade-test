# 五年 Python 實測驗算：150 分類批次、14,816 配置 — 2026-10-31

本輪在聊天 Python 執行環境中執行 `trade_test_incremental_5.py`，對 GitHub Actions run `41068912974` 新下載的五個 ZIP 工件逐筆獨立重算已保存五年交易收益，並與既有去重清單 138 批合併。沒有使用 Jules、沒有新增 workflow，也沒有變更 main。

## 本輪新取回的 GitHub 工件

| 商品與時區 | Artifact ID | 解析出的完整策略分類 | 逐筆重算結果 |
| --- | ---: | --- | --- |
| SOLUSDT 45m | 13010799751 | original, compound, fixed, new | 384/384 |
| SOLUSDT 10m | 13010219502 | original, compound, fixed, new | 384/384 |
| SOLUSDT 15m | 12996847040 | original, compound, fixed, new | 384/384 |
| ETHUSDT 30m | 12994495652 | original, compound, fixed, new | 384/384 |
| ETHUSDT 15m | 12994333348 | original, compound, fixed, new | 384/384 |

五件工件各四分類，共 20 個分類工件，其中 8 個已在先前 138 批驗證清單，**淨增加 12 個不重複分類批次**。按 `(symbol,timeframe,family)` 去重後，從 **138 → 150** 批、五年排名配置從 **13,664 → 14,816**，原樣本加上新樣本共 **14,816/14,816** 個配置逐筆 R 線性收益回算完全吻合，**0 個收益不一致、0 個解析錯誤**。

每份檔案已檢查 `manifest.start_utc` 為 2021-10-10、`end_exclusive_utc` 為 2026-10-10；`ranking.csv`、`trades.csv` SHA256 均與 manifest 相符。收益公式 `max(-100, risk_pct * sum(first N trade R))`，依照原始固定初始資金風險模型而不是複利。

使用的 Python 腳本：本輪工作容器 `/mnt/data/trade_test_incremental_5.py`。已產出完整去重查核清單：`/mnt/data/TradeTest_incremental_5_merged_20261031.csv`（150 行）；這是此對話可下載的沙盒檔案，不表示 CSV 本身已上傳 Git。

**驗證邊界：** 本輪是驗證已存五年 OHLCV 訊號產出的 trades/rankings 與獨立收益重算，不是新增五年行情、也未從原始 OHLCV 重新發出每一個入出場訊號；沒有完成全部 Kelly、最大回撤獨立驗證。舊的 124 批 Git 嚴格驗收集合與本輪 150 批有重疊，不可兩者相加。全部 9 商品×17 時區×4 分類共 612 個分類批次與 31 舊＋7 新策略碼缺口仍未完成，維持 `partial`，絕不可標示全部完成。
