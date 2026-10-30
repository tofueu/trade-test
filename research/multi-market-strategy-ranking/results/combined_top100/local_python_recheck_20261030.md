# Trade Test — 五年 Python 新舊策略增量回測／驗算進度

**更新：2026-10-31（臺灣時間）。狀態 PARTIAL：全部五年策略尚未完成。**

## 目標與不可重跑規則

- 五年真實回測窗口：**2021-10-10 UTC 至 2026-10-09 UTC**（end-exclusive 2026-10-10 UTC）。
- **只測 9 個指定市場**：BTCUSDT、ETHUSDT、SOLUSDT、黃金 GC=F、白銀 SI=F、美國指數 ES=F/NQ=F、臺灣 ^TWII、USDJPY=X。
- **只測 17 個指定週期**：1m、2m、3m、5m、10m、15m、20m、30m、45m、1h、2h、3h、4h、6h、8h、12h、1d。153 市場×週期對；612 策略分類欄位是工作清單，不等於已全部測完。前版 225 對包含未指定秒線／週月線，已修正。
- **31 種舊策略 + 7 種新策略**。先按 Git 既有完整 `manifest.json`、`ranking.csv`、`trades.csv`、OHLCV SHA256、成功 artifact 去重，不能因 workflow 整體失敗就重跑已產生的完整批次。**舊策略日線已跑，絕不重跑 1d。**
- 禁止交 Jules 1／Jules 2；禁止新增 GitHub workflows、禁止修改 main。六小時自動驗收任務已設定 Git+其 ChatGPT 任務對話定期回報，無法把普通聊天中的 Python 誤稱為無限期背景常駐執行。

## 本輪真實 Python 驗算成果

- 從既有 GitHub Actions 已完成的五年成交 R 序列與 `ranking.csv / trades.csv / manifest.json` 原始 ZIP 取回，檢驗 **完整 SHA256**，重新計算前四年 IS Kelly、五年成交次數、收益、最大回撤及出場/倉位風險。
- **目前驗證 124 批、12,720 配置，數值不一致 0**。已完成者保留 checkpoint，不重跑訊號；本輪是在本地重新驗算**已保存的實際成交資料**，不是本地重新取得所有五年 OHLCV 後重新產生進場訊號。
- 新驗出的 SOLUSDT 真實五年 1d／4h／12h／6h／8h／2h，四類（original、compound、fixed、new）均完成 SHA 與逐筆重算；既有完成之 BTC 1m original/compound/fixed、ETH 1m/3m/5m 四分類亦已驗算。
- **153 對指定市場×週期中，34 對具本機實際成交證據，22 對具四分類成交回放**。這些計數只代表可獨立驗算的成交證據，不代表其他市場／時區已完成五年訊號回測。
- **收益 Top100** 已按僅指定市場、實際五年成交 ≥70 筆、總收益 >100%、實際風險 >0 且 ≤ 前四年 IS Kelly、最大回撤 ≤100%、品種+週期+策略+出場方式去重。**98 筆本機實際交易 R 回放，2 筆原 Git 歷史快照**（明確標示 `本機已驗算=false`）；38 策略家族榜保留所有家族，歷史來源或非指定商品的家族最優者有明確標記，不能算這次新完成。
- 最新榜首 BTC 8h Volume_Donchian20 +1,879.65% /117 筆；第3位 SOL 2h Supertrend+EMA200 +1,512.35% /600 筆，均僅為研究回測、非實際交易保證。**伯努利 iid 尚未證明，TradingView/Pine 逐筆 parity 尚未驗證。**

## 程式修補／避免重複測試

- 現有 `tools/run_legacy_all_timeframes.py` 漏了指定的 20m；已修補 `20m=(5m,4)` 只允許 4 根連續真實 5m K 線組合並嚴格核對時間戳與缺口；commit `5e87bbbf164cc1ffa17a9eaab6076a0539d44a75`。
- [逐格 612 欄位去重清單](five_year_deduplicated_worklist_17timeframes.csv)：**124 項完成且 SHA+逐筆驗算，列為 `SKIP_RETEST`**；剩餘 488 欄位不表示都可執行，例如非加密市場五年分鐘 K 線來源未獲驗證、舊日線已有歷史快照免重跑、仍有既有 run 正在進行及原始行情品質不合格。不能把未取得真實五年 OHLCV 的項目填入捏造績效。
- 數據曾出現 SOL 月檔缺漏，既有 Python 來源僅允許從相同 Binance 商品的每日歷史 ZIP 修補且需保留檔案 SHA；^TWII 農曆年交易所休市不可合成假K；USDJPY Yahoo 異常高低價不可改造來算收益。

## 最新 Git 成果連結

- [只限指定市場的五年收益 Top100](local_python_kelly_top100_20261030.csv)。
- [全部 38 種策略家族順位／資料來源](local_python_38_families_20261030.csv)。
- [17 週期、153 市場×時區驗算覆蓋表](local_python_full_market_timeframe_coverage_20261030.csv)。
- [逐格去重清單，已完工不重跑](five_year_deduplicated_worklist_17timeframes.csv)。

## 尚未完成

既有 Python run [41068912974](https://github.com/tofueu/trade-test/actions/runs/41068912974) 的 SOL 其他分鐘／小時週期及 BTC 衍生 2m、10m、45m、3h 等仍要逐件取得完整五年工件與 SHA 驗證。當前對話 Python 工作環境無完整五年 OHLCV 且無對外直接行情網路；只能對可取回的已跑五年成交工件作獨立重算與排名，**不能聲稱全部策略的原始五年訊號重跑已完成**。每六小時檢查剩餘真實成果並更新 Git 與自動任務對話。
