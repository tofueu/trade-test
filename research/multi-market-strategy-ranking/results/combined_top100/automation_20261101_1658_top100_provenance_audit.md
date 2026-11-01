# Trade Test 增量稽核｜2026-11-01 16:58 Asia/Taipei

## 本輪實際作業
使用 GitHub connector 從既有隔離分支直接取得 `local_python_kelly_top100_20261030.csv` 全文，依 CSV 表頭解析並以 JavaScript 重新統計 100 列；另讀取 `local_python_38_families_20261030.csv` 與既有 `tools/run_legacy_all_timeframes.py`。本輪未取得五年原始 OHLCV，未執行 Python 訊號回測，未重跑舊 1d。

## Top100 出處與驗證層級（本輪新增的具體稽核結果）
- 總列數 100；以 商品×週期×策略分類×策略×出場方式×倉位法 去重後 100 列。
- 商品：SOLUSDT 63、BTCUSDT 22、ETHUSDT 14、SI=F 1；其他指定五市場 0 列（不代表已完成或不合格）。
- `原始狀態`：`trade_fills_replayed_locally_sha256` 98 列；`complete_sha256_verified` 2 列。**98 列屬舊交易回放，不得當成新 OHLCV 訊號回測。** 後兩列仍須核對其 manifest、逐筆交易與行情來源，不能只靠狀態字串視為完成。
- 100 列均有「原始行情SHA256」欄位值，但本輪未取得原始 OHLCV bytes 重新雜湊，不能稱行情獨立驗證。
- `實際風險_pct > IS_Kelly_pct + 1e-8`：0 列。
- iid 狀態：`iid_not_rejected_not_proven` 96 列、`iid_runs_rejected_at_5pct` 2 列、`not_tested_no_trade_by_trade_IS_outcomes` 2 列；**0 列可以宣稱 iid 已證明**。
- 本輪新跑五年 K 線策略訊號組合：**0**；舊交易回放新增：**0**；獨立行情 SHA 新增：**0**。
- completed/required（market×timeframe×family×strategy×exit）：**未能可靠計算**，因尚缺全量 manifest+artifacts 逐配置合併與原始行情驗證，不能以排行榜列數代替。

## 去重及執行限制
- 僅九市場與指定 17 週期。舊31策略×九市場×1d 全部鎖定禁止重測；只允許既有基準驗收。新7策略 1d 只補缺口。
- `run_legacy_all_timeframes.py` 位於 `research/multi-market-strategy-ranking/tools/`；本輪確認可讀，但沒有真實行情可執行。
- 優先取回 ETH 1m/3m/5m artifact 與 BTC 1m original/compound 的 manifest/CSV；對已完成配置不重跑。對 SOL 缺口先用 Binance 真實日封存驗連續性；20m 僅由連續四根真實5m聚合。
- 不交 Jules、不新增 workflow、不動 main、不覆蓋 checkpoint。

## 既有榜
- [38 家族榜](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)

本輪沒有新的 Python 五年訊號結果，故不更新排名數值；上述為既有榜的 provenance 分類驗證，不是完整回測完成證明。
