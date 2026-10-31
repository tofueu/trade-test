# 真實五年行情恢復：實際原始工件檢查 — 2026-11-01

本輪直接在聊天執行容器使用 Python 和 GitHub Connector 對歷史 Jules/Actions 工件做檔案檢查，與只查排名不同。

1. 從 GitHub Actions run 41064675326 下載大型合併工件 `old-new-python-five-year-audit-and-top100`（artifact ID `12990575827`；ZIP 約 233.6MB）。
2. Python `zipfile.ZipFile` 成功解壓檔名索引，**154 個檔案**，內容包括 `all_timeframes/legacy_BTCUSDT_*/checkpoint.json`、`manifest.json`、`ranking.csv`、`trades.csv`；逐項搜尋檔名中的 `ohlcv`、`klines`、`candle`、`market_data`，**0 個原始 K 線候選資料檔**。
3. 確認目前 Git 分支的原始五年行情快取目錄 `research/multi-market-strategy-ranking/src/five_year_market_data/` **不存在（Git contents 404）**；現存的是原始行情來源取得程式 `src/run_intraday.py`、`src/five_year_multi_market_kelly.py`。
4. `run_intraday.py` 原始程式確實設計從 `https://data.binance.vision/data/futures/um/monthly/klines/` 抓取 BTCUSDT/ETHUSDT/SOLUSDT 各月 ZIP，並以每日 ZIP 补齊 2026-10-01..09；20m 是 5m K 棒每 4 根聚合，不是憑空補 K。
5. 本地 Python `socket.getaddrinfo` 實際測試 `data.binance.vision`、`raw.githubusercontent.com`、`query1.finance.yahoo.com` 都是 `gaierror [Errno -3] Temporary failure in name resolution`，因此此聊天容器不能直接從公開網址取得缺少的行情。
6. 本輪**新增原 OHLCV 訊號回測數量 0**。已存交易回放完成數 188 分類批次不變，不可當成新策略訊號成果。五年策略全部組合 **仍未完成**；未編造 K 棒、未跑舊策略重複批次。
7. 下一個真正可執行步驟：在有網路且可存檔的 Python 執行主機，使用現有 `run_intraday.load_real_ohlcv` 下載並持久保存行情快取與 SHA；從未測的 20m 以及 BTC 新策略缺口起依 `tools/run_legacy_all_timeframes.py` 逐批執行，再記錄逐批 `trades.csv`、`ranking.csv`、`manifest.json` 到同隔離分支。不能將本 GitHub Actions 工件誤認已有完整原始 K 線。用戶禁止交 Jules；不改 main，不新增 workflow。
