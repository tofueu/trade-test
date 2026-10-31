# ETHUSDT 3h 五年獨立 Python 逐筆收益回放 — 2026-10-31

## 真正執行的檢查

- 從 GitHub Actions run `41068912974`、artifact `13009351170` 下載 `market-ETHUSDT-3h` ZIP 並在 Python 打開內層 tar.gz。原始五年 OHLCV 時段：`2021-10-10T00:00:00Z` 到 `2026-10-10T00:00:00Z` (exclusive)。
- 讀入 original / compound / fixed / new 四類 `manifest.json`、`ranking.csv`、`trades.csv`。四類 ranking 與 trade SHA256 全部吻合 manifest。
- 依照 `(策略, 出場方式)` 分組逐筆 R，按照各排名配置的「實際風險_pct」及「五年交易數」截取每筆成交，以**初始資金固定風險、R 線性加總**重算收益；資金跌破 0 時五年收益以 **-100% 截斷**。公式：`max(-100, risk_pct * sum(first N trade_R))`，符合原始固定1R / Kelly / 半 Kelly / 四分之一 Kelly 排名執行的資金口徑。
- original **288/288**、compound **32/32**、fixed **36/36**、new **28/28**，共 **384/384** 列五年收益與原始排名吻合，數值誤差容忍值 `1e-6` 百分點，**0 不一致**。
- 內含 **40,459 筆存檔逐筆交易 R** (original 30,942; compound 4,419; fixed 3,419; new 1,679)。每列的已成交 N 不應與整份 trades 檔數量混淆。
- 最初用複利模型驗證只有 192/384 吻合，經對照發現原始回測是「固定初始資金風險的線性 R 口徑」，改正後 382/384；最後兩筆為資金歸零、原排名將收益截斷 -100%，加上截斷後 **384/384 全數吻合**。
- **驗收範圍**：確認已存結果的五年收益可以由實際逐筆 trade R、風險百分比、成交筆數與正確截斷規則獨立重建。**並非重新從 OHLCV 生成入出場訊號**；尚未重算全部排名列的最大回撤與 Kelly 的 IS 統計，故不能宣稱所有風險統計全部獨立驗證。
- 請在完整去重清單把 ETHUSDT 3h 四類從 PENDING 註記為「五年完整交易工件 + SHA256 + 五年收益逐筆回放已通過」，不要重跑 ETH 3h 五年訊號；合併 124 批基準時應先核查有無既有批次重複，不能直接累加為 128。

獨立 Python 回放完整明細：會話檔案 `/mnt/data/trade_test_ETHUSDT_3h_replay_20261031.csv`，384 列，各列附 reported/replayed returns/error 與 SHA 狀態。執行碼：`/mnt/data/trade_test_eth3h_replay.py`。不能把 ChatGPT 暫存路徑誤當 Git 上已有 CSV。

Git 主分支不更動、不交 Jules、無新 workflow。專案**仍未完成所有組合**。
