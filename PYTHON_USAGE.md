# Python 取用：Supertrend_ADX20

本分支用於保存 Python 原始回測策略，Pine 用於之後交叉驗證。

## 檔案與配置

- [strategy.py](strategy.py)：原始共用引擎副本，內含本策略；不是已鎖定本排名配置的獨立交易機器人。
- [strategy_config.json](strategy_config.json)：本排名名稱、商品／週期、原始排名完整欄位、來源 manifest；未找到證據的欄位不補猜。
- [原始策略模組](research/multi-market-strategy-ranking/src/run_strategies.py)：`make_state()`；使用策略名稱 `Supertrend_ADX20`。原單指標家族由原始 `STRATS` 名稱映射。
- [共用指標與 Kelly](research/multi-market-strategy-ranking/src/five_year_multi_market_kelly.py)
- [共用出場回測](research/multi-market-strategy-ranking/src/five_year_exit_method_sweep.py)
- [多週期入口](research/multi-market-strategy-ranking/tools/run_legacy_all_timeframes.py)

## 下載與執行

請下載整個分支，保留 `src/` 與 `tools/` 目錄，使用原始 [requirements.txt](research/multi-market-strategy-ranking/requirements.txt) 安裝 numpy、pandas。原始入口指令：

```text
python research/multi-market-strategy-ranking/tools/run_legacy_all_timeframes.py --symbol ETHUSDT --timeframe 6h --family new
```

原入口按家族執行，會產生同家族多個策略／出場配置；以 `Supertrend_ADX20` 及 JSON 中保存的出場方式、倉位法篩選結果。它沒有單策略旗標，沒有新增假旗標。

## 後續交易軟體接入

原模組中部分有頂層批次回測，請勿直接將 `import strategy` 當成無副作用的即時訊號 API。原多週期入口的 `load_legacy_definitions()` 已能僅載入指定原始定義；可沿用該方式再開發交易系統。行情、訂單、成交同步及即時保護單仍需另行實作，現有程式是歷史模擬。

## 驗證狀態

已從本機原始 ranking.csv 找到收益與交易數相符的配置，完整原始欄位及 manifest 保存在 JSON；這是來源追溯，不是本次重新回測。

本機較新的 run_intraday.py 有語法錯誤，本次沒有將損壞版本覆蓋上去；分支中保留的資料模組尚未完成端到端驗證。GitHub 下載後不能僅憑來源同步就認定回測可完整重現。既有成果有 manifest/checkpoint 去重機制；已有完整結果時入口可能直接跳過執行。

本次整理不修改 Python 交易規則、成本或 Kelly 計算，也不修改 Pine。
