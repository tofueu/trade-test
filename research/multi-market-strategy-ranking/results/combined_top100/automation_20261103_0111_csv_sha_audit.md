# Trade Test 2026-11-03 01:11 +08:00 實體工件 SHA 驗收

本輪使用 Python 直接下載後解壓及串流計算 4 件 GitHub Actions ZIP（BTC 1m original、ETH 1m/3m/5m），共檢查 13 份 family manifest。13 份 ranking.csv 與 13 份 trades.csv 的實際 SHA256 均與 manifest 宣告相符；逐檔交易資料列數亦與 manifest 相符。

- 本輪新增實體 CSV SHA256 通過：26 份（13 ranking + 13 trades）
- 本輪新跑五年 OHLCV 策略訊號：0 組；舊交易重播：0 組
- 13 份 manifest 合計交易 CSV 18,427,288 列；宣告測試出場 744，宣告已保存出場 360（**非全市場完成數**）
- 五年 OHLCV SHA256 僅為 manifest 宣告，未取得原始 OHLCV 重新計算；因此不能把 CSV SHA 通過等同於五年 K 線訊號獨立重算
- ETH 1m、3m、5m 的 original / compound / fixed / new 以及 BTC 1m original 已完成這一層 CSV 驗收；BTC 1m compound 在前輪已驗證，不重跑
- 舊策略九市場 1d 不重跑。未交 Jules、未新增 workflows、未動 main
- 完整 market×timeframe×family×strategy×exit 的 completed/required 尚未核定，需跨其他 artifacts 去重，不能用這 13 份宣告取代全域完成證據
- 既有排行榜保持不變： [38 家族榜](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_38_families_20261030.csv) / [Kelly Top100](https://github.com/tofueu/trade-test/blob/report/trade-test-multi-market-20261030/research/multi-market-strategy-ranking/results/combined_top100/local_python_kelly_top100_20261030.csv)

下一步：取得原始 K 線檔獨立驗 OHLCV SHA；彙整全部 manifest 的逐配置去重清單；確認 SOL 真實 daily ZIP 缺口後只跑缺失配置。未通過完整驗證不得宣稱回測完成。
