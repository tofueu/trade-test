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


## 2026-10-31 04:13 臺灣時間：本輪 GitHub API 與失敗日誌實際複核

- **本輪新增已驗證批次 0**；已確認基準仍為 **124/612 批 SHA256 + 成交 R 回放**，12,720 個已驗算配置，數值不一致 0。這是前次已保存驗證結果，不是本輪重新跑五年 OHLCV 訊號。五年範圍仍為 2021-10-10 至 2026-10-09 UTC；9 市場、17 週期，絕不回測已完成的舊 1d。
- [BTC 舊策略 Run #41064675326](https://github.com/tofueu/trade-test/actions/runs/41064675326)：整體 GitHub 結論 `failure`，但 API 已列出 **37 個未過期 artifact（36 個舊策略 market×timeframe×family + 1 個彙總）**；首 30 個 jobs 都為 success。**不能因整體 run 失敗而整批重跑**。先前已 SHA/交易 R 驗算 36 個 BTC 批次，後續只檢查缺漏。
- [ETH/SOL/傳統市場 Run #41066783962](https://github.com/tofueu/trade-test/actions/runs/41066783962)：整體 `failure`；首 30 jobs 16 success、14 failure，31 個未過期 artifact。已保存的 ETH 1m、3m、5m 完整分類已納入既有 124 批驗算；不可重跑。**SOL 失敗工件僅 293 bytes 的錯誤報告，不是完成交易資料**。實際失敗 job 124100613731：`RuntimeError: Irregular or missing five-year candles; no qualified ranking`。修復須從 Binance 同標的同週期真實 daily archive 補回缺口並重新驗 SHA、時間戳；不得補造 K 線。
- 台灣 ^TWII 1d 失敗 job 124100616387：`UNAVAILABLE_YAHOO_LONG_GAP: ^TWII 13 days 00:00:00`，須依交易所休市曆確認春節長假，而非合成 K 線；**保留先前舊日線基準不重測**。USDJPY=X 1d 失敗 job 124100616569：`UNAVAILABLE_INVALID_YAHOO_RANGES: USDJPY=X`，須換用可稽核的真實 OHLCV 來源並保留錯誤紀錄，不得修改異常價造出績效。
- [續跑 Run #41068912974](https://github.com/tofueu/trade-test/actions/runs/41068912974)：GitHub run API 顯示 `queued`，但 job API 首 30 項已見 **26 success、3 in_progress（SOL 1m、BTC 2m、ETH 2m）、1 queued（SOL 2m）**，且已有 **27 個 artifact**。**這 27 個只有存在性證據，尚未逐一下載驗 SHA / trades / manifest，不計新增已完成**；不得覆蓋 checkpoint 或對在跑批次重複派工。
- 原分支 [latest_verification_manifest.json](latest_verification_manifest.json) 仍 `status=partial`、`completed_legacy_timeframe_family_batches=6/36`（舊報告欄位，未同步已收取 36 個 artifact），`verified_multi_asset_batch_count=24`；另有 124 批更完整的獨立逐筆回放去重帳本 [five_year_deduplicated_worklist_17timeframes.csv](five_year_deduplicated_worklist_17timeframes.csv)。**三者證據層級不同，不得混稱 612 已完成。**
- [收益 Top100 CSV](local_python_kelly_top100_20261030.csv) 及 [38 家族榜 CSV](local_python_38_families_20261030.csv) 本輪確認均存在；**未新增可驗算成交，因此不改寫兩榜數值**。Top100 中 98 筆可追溯已驗算成交、2 筆為歷史快照待證；五年 ≥70 筆、收益 >100%、實際風險 ≤ 前四年 IS Kelly 是排名門檻。伯努利 iid 與 TradingView/Pine parity **未驗證**。
- **本輪處置：**已實際取回 SOL、^TWII、USDJPY 三種失敗 job logs 並定位根因。避免重跑已完成日線及已驗批次，也避免對仍進行中的 run 再啟動同批次。本輪無新增 Python 五年行情訊號回測；沒有足夠完整原始 OHLCV 供本地重跑。下一步收取續跑中真正完成的缺口 artifact，逐件核對 `manifest.status=complete`、`ranking.csv`、`trades.csv`、OHLCV SHA 與成交 SHA，再增量併榜；若 job 真正失敗才考慮單 job 重試。


## 2026-10-31 09:26（臺灣時間）— 本輪實際 GitHub Job Logs 排錯與去重驗收

- **進度不虛增：124 / 612 個市場×週期×分類批次已具 SHA256 + 逐筆交易 R 回放證據；12,720 個既有配置已驗算。新增本輪完整 SHA + 成交回放批次 0。** 本輪未取得原始五年 OHLCV 供 Python 訊號重算，不得把 Actions Job success 當作本輪已完成的 SHA 驗收。
- 本輪重新查詢 GitHub Actions：#41064675326 = **36 個計算 Job success、1 個 publish failure、37 個 artifact 可取**。publish log 證明已下載 36 個 artifact、產生 commit `2eff31d`，但 push 發生 **HTTP 408 RPC timeout**，不能當作 Git 分支已成功收錄 36 批。這是發布失敗，**不是 36 批回測失敗**；禁止整批重跑，應只收取既有 artifacts 並逐個核對其內 `manifest.json(status=complete)`、`ranking.csv`、`trades.csv` 及 SHA256。
- #41066783962 = **16 個 Job success、15 failure（包含 14 個市場計算失敗與 1 個發布失敗）、31 個 artifact**；其中 ETH 1m/3m/5m 有既有完整結果。發布 Job 下載 30 個 artifacts 後在 git cherry-pick commit `6c4199d` 失敗；不能重跑成功的 ETH 計算。
- #41068912974 = **41 個 Job success、2 failure、43 個 artifact**。publish Job 下載 42 個 artifacts 時出現 `legacy_BTCUSDT_1d_compound` ZIP 解壓到同名 `checkpoint.json` 的碰撞；最後 git push 再發生 **HTTP 408 RPC timeout**。應分離每個 artifact 的解壓目錄、以 manifest/checksum 去重後，改用小型逐檔提交避免大型成果 push 超時；舊 1d 不重算。
- USDJPY=X 1d 失敗 Job #124179330079 的確切例外：`ValueError: UNAVAILABLE_INVALID_YAHOO_RANGES: USDJPY=X`；其 298 bytes artifact 是錯誤證據，不是有效五年交易結果。不能用假價修補。
- 目前隔離分支 `latest_verification_manifest.json` 仍是 `status=partial`、`completed_legacy_timeframe_family_batches=6`、`required_legacy_timeframe_family_batches=36`；**Git 已有 36 個計算成功 artifacts ≠ 此份總 manifest 已驗收 36/36**。已驗證的 BTC 1m original/compound、ETH 1m/3m/5m 在 124 批工作清單中保留 SKIP_RETEST。
- 排名沿用既有 [全 38 策略家族 CSV](local_python_38_families_20261030.csv) 及 [Kelly 條件 Top100 CSV](local_python_kelly_top100_20261030.csv)，沒有新驗證交易可安全改動收益數字；Top100 98 筆成交回放＋2 筆歷史快照仍待分開標示。**伯努利 iid 與 TradingView parity 未驗證。**
- 下一個可執行修復：下載未收取的成功 artifact，於獨立目錄驗 `manifest/ranking/trades` SHA；僅把新通過的批次增量併入排行榜和去重表；修復 artifact 解壓檔名衝突、發布改小批次提交。非加密市場五年分鐘 OHLCV 未證實仍標 unavailable；不碰 main、不交 Jules、不新增 workflow。
- 本輪使用 GitHub connector 實際讀取三次 workflow 的 Job 列表、artifacts 清單及 4 份失敗 Job logs；**未在本輪取得可直接由 Python 載入的五年行情／成交 ZIP 位元組**，故沒有宣稱完成新的 Python 回測。
