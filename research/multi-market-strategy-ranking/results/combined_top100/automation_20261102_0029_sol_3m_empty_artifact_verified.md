# Trade Test 增量驗收 — 2026-11-02 00:29 +08:00

## 本輪實際 Python 驗證
- 來源：Run #41066783962，artifact id 12985660219，market-SOLUSDT-3m，GitHub API 回報 295 bytes、未過期。
- 已實際下載 ZIP 並以 Python zipfile、tarfile、hashlib 解包。
- ZIP SHA256 = `fe3959b35a0060782ca5628088ac7fe0507c91f27e72724963377a926ccea6e9`，與 GitHub artifact digest 一致。
- ZIP 僅包含 `market-SOLUSDT-3m.tar.gz`（139 bytes）；tar.gz 僅有空目錄 `multi_SOLUSDT_3m_original/`（0 bytes），**無 manifest、ranking CSV、trades CSV**。
- 結論：這份 SOLUSDT 3m artifact 是「存在且外層 SHA 驗證通過，但內容為空」，**不得列為已完成回測**。不代表 SOL 所有工件都空，也不能推定行情一定缺失。

## 完成數與分類
- 本輪新跑出五年 OHLCV 策略訊號組合：**0**。
- 本輪舊交易紀錄回放：**0**。
- 本輪新增外層 artifact SHA 驗證：**1**；新增內層交易 CSV SHA 驗證：**0**。
- 全域 completed/required：尚未從全部 manifest、逐筆交易與 K 線 SHA 完整去重，**不報虛假完成率**。
- 已存在工件 ≠ 已驗交易回放 ≠ 已完成五年原始 K 線訊號回測。

## 後續具體修復
1. 對 SOL 其餘極小工件逐一解包，不得直接依檔案大小判定錯誤。
2. 追查 SOL 3m 工作日誌與原始 Binance archive 的缺日；以真實 daily archive 補齊且核對 OHLCV 連續性與 SHA 後，才對缺失配置執行 Python 回測。
3. 建立 market × timeframe × family × strategy × exit 唯一鍵總表；舊 31 策略九市場 1d 全部禁止重跑。
4. 維持兩份既有排行榜，不將空工件或舊交易重播算作新策略成果；伯努利 iid 未證明。

## 既有排行榜（尚未完成全量驗收）
- [38 家族榜](local_python_38_families_20261030.csv)
- [Kelly Top100](local_python_kelly_top100_20261030.csv)

未交 Jules、未新增 workflow、未動 main；只在既有隔離分支寫本報告。
