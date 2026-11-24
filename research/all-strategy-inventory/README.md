# 全部既有策略測試盤點（截至 2026-10-20）

本頁把先前討論過的策略分成「已有可核驗績效」與「測試/產物待補」。不同商品、週期、倉位和回測假設不合併成一個收益排名。只有同一資料期間、同一計算口徑的測試才可直接比較。

## A. 可核驗的每日線五年總榜

- GitHub 草稿 PR：[加入策略規則、回測程式與五年收益排名](https://github.com/tofueu/trade-test/pull/1)
- 前 50 名：[overall_top50.csv](https://github.com/tofueu/trade-test/blob/codex/strategy-ranking-20261011/research/multi-market-strategy-ranking/results/overall_top50.csv)
- 總榜：9,556 列、32 種訊號規則、26 個商品；含四個策略家族。
- 期間：2021-10-10 至 2026-10-10 UTC；最後一年作 OOS。
- 程式、成本、SL/TP、倉位假設與限制見同一分支的 [README](https://github.com/tofueu/trade-test/blob/codex/strategy-ranking-20261011/research/multi-market-strategy-ranking/README.md)。
- 這是歷史模擬。前 50 有些策略交易筆數少、部分 OOS 負收益，且包含全凱利欄位；排名不能直接當實盤建議。

四個家族包括：單指標出場變體、雙指標/週線複合、固定盈虧策略、新增趨勢/突破/均值回歸策略。前 50 CSV 是這些每日線測試的總排名；它不包含其他週期的測試。

## B. 曾回報、但尚未能由 Git 產物重現的 H1 測試

先前報告過 5 種規則 × 3 個商品，共 15 組：Ichimoku Kijun/Cloud、DMI_ADX20、WilliamsR_EMA200、CCI20_EMA200、ROC10_EMA200；商品為 USD/JPY、Gold、US500。當時使用 H1 行情，另有初始止損與固定風險等假設。

目前此總榜分支沒有找到該 H1 測試的程式、行情 manifest、逐筆交易或資金曲線。故此 15 組目前只列為「待恢復/重跑」，不併入 A 的每日線排名，也不把先前對話中的數字當作已驗證成果。補齊程式、原始資料及輸出後，會建立獨立 H1 排名表。

## C. SMC 多時區策略

- 最新五年測試工作流狀態見 [SMC PR #47](https://github.com/tofueu/trading-strategy-multi-timeframe-backtest/pull/47)。
- PR 記錄顯示：曾有連續行情驗證未補齊 80 根 BTCUSDT 1m K 線，後續 API 請求遇 HTTP 451；因此未進入交易模擬，沒有五年交易績效產物。
- 相關 Draft PR 的 pytest 成功只證明程式測試通過，不等於行情回測成功。
- SMC 過往大規模 sweep 未找到可驗證的排名/交易產物，所以不放進收益排名。待完整行情與正式策略產物保存後再納入獨立測試區。

## D. Daranwu 作者策略

- 作者來源：[Dcard 作者頁](https://www.dcard.tw/@daranwu)；研究倉庫：[tofueu/daranwu-strategy-research](https://github.com/tofueu/daranwu-strategy-research)。
- 目前本工作階段的 GitHub 連接器回傳 422，無法驗證該倉庫最新 PR/程式/產物。之前盤點指出出場、止損與倉位配置規則仍需作者公開證據補足。
- 因此目前不把它列作已完成的五年績效排名；取得可讀的規則、程式、行情與逐筆輸出後再另列。

## E. 殖利率策略、15m RSI 與 5m 均線策略

這些策略在先前對話中有提出測試需求，但本次盤點未找到可核驗的回測程式、數據 manifest 或交易輸出。先列為「待確認/待測」，不編造收益或排名。找到相應 repo/PR 或完整產物後，再納入各自的週期排名。

## 後續納入排名的最低證據

每組需保存策略程式及版本、商品/週期、行情來源與覆蓋區間、缺口檢查、成本與倉位假設、逐筆交易、資金曲線，以及收益、CAGR、最大回撤、PF、勝率、交易數、止盈/止損數。缺少其中足以改變結果的關鍵資料時，標記為未驗證，不與已完成策略混排。
