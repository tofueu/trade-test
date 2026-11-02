# Trade Test 增量驗收｜2026-11-02 09:46 Asia/Taipei

## 本輪真正執行
- 透過 GitHub connector 下載 Run #41064675326 的 `legacy_BTCUSDT_1m_original`，Artifact ID 12990135479，ZIP 112080486 bytes。
- 本地 Python 以 hashlib.file_digest 獨立驗 ZIP SHA256 = `54324a419f95bbd31c4da3dd2ab50c800334e4cb587033ba3339ad637e5a98bc`，與 GitHub digest 一致。
- 解壓 ZIP 檢查 `checkpoint.json`, `manifest.json`, `ranking.csv`, `trades.csv` 四個檔案；manifest `status=complete`, `BTCUSDT`, `1m`, `original`。
- manifest 記載 UTC 2021-10-10 至 2026-10-10 (end-exclusive)，2629440 根 K 線，missing_or_irregular_intervals=0，ohlcv_sha256=`189c4856bba7a5e053aca8d2f4fc08eb9a2ddbede15c766051e5e5628d57b442`。注意：這是 manifest 聲明，未重新下載 OHLCV 獨立驗證。
- Python 逐塊解壓完整 CSV 並重新計算 SHA256：`ranking.csv` = `7e9097fca05cdcb7e74a1532c10108c433255b80459b27127b24fcbe51e61217`（288 列）；`trades.csv` = `2ed4721adbfa5b48e379fd8af2e45fd73dd7b099e1a484d5ada28b1d0e79a473`（6222051 列）。兩者與 manifest 相符。
- manifest 列出 8 種策略，每種 tested_exit_count=9、saved_exit_count=9；ranking 288 列並不直接等於 288 個獨立策略訊號配置，因還有倉位法維度。不得重跑此已保存批次。
- 本輪新跑五年策略訊號組合 **0**；舊交易回放 **0**；獨立驗證 ZIP 1、CSV 2；本輪新增 SHA 驗收涵蓋 BTCUSDT 1m original。
- Git tree SHA `b72048a9e1099b53a8c1447865872ac8c02c3a72` 共 351 項，發現 30 個既存回測 manifest 加 1 個 latest_verification_manifest。其餘未完成的市場×時區×策略×出場唯一鍵仍待完整驗收，completed/required 不虛報。
- 不重跑任何舊策略 1d；未交 Jules，未新增 workflow，未動 main。

## 下一輪
優先獨立下載驗證 BTC 1m compound、ETH 1m/3m/5m 的 ZIP 與內部 SHA，對全部保存工件建唯一鍵去重清單；僅對真正缺失且具五年真實 OHLCV 的組合補跑。SOL 缺口須先由 Binance 真實 daily archive 修復並驗 SHA。

## 排行榜（仍為歷史榜，非全量完成）
- [38 家族歷史榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv)
- [Kelly Top100 歷史榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)
