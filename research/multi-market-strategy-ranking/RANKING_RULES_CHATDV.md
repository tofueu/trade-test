# Trade Test 排名規則｜交接 ChatDV（2026-11-02）

> 本文件將 **Git 現存 Python 排名實作** 及使用者歷次確認的驗收條件整理為單一明確規格；**不代表已完成所有五年測試**。嚴禁以缺失資料填零、虛構交易、以舊工件回播冒充重新執行策略。

## 一、母體與測試前提

- 五年 UTC：`2021-10-10 00:00` ～ `2026-10-10 00:00`（尾端不含）。每個市場×週期×策略都需來源可查的真實 OHLCV、交易紀錄、版本與散列；衍生週期必須由較小真實 K 棒且無缺口地聚合。
- 9 市場：`BTCUSDT, ETHUSDT, SOLUSDT, GC=F, SI=F, ES=F, NQ=F, ^TWII, USDJPY=X`。
- 17 週期：`1m,2m,3m,5m,10m,15m,20m,30m,45m,1h,2h,3h,4h,6h,8h,12h,1d`。
- 舊策略**已完成的日線直接沿用、不重新測試**；其他已通過實際訊號回測與來源驗證的批次也去重。新策略僅補未完成的。不可因某一行情缺失停止其他可執行組合。
- 策略總數需對帳：近期使用者指定 **40 種為目標**；歷史記錄另有「舊 30＋新 7」及「舊 31＋新 7」互相矛盾。Git 主 runner 現僅實作 original 8、compound 8、fixed 9、new 7 個分類內槽位（舊策略跨類有重名）；不能以改名或複製補湊 40。先在總表明列已實作／缺規則／不重名的真正策略數量，再逐個恢復。

## 二、合格 Top100 門檻（依現有 `tools/aggregate_all_timeframes.py` 第 209–242 行）

對每個有完整真實回測的配置，先計算欄位：

- `五年交易數 >= 70`。
- `五年收益_pct > 100`（**嚴格大於**，不是等於）。
- `最大回撤_pct` 必須在 **0 到 100（含）** 的合理範圍。
- `可交易 = True`；現有程式將 `^TWII` 作不可直接交易的訊號基準，不應納入「可交易收益 Top100」，但仍須保留策略測試紀錄。
- `資料完整標記 = True`，且 `資金停止 = False`。缺原始來源、缺必需交易檔案、檢查未通過者不得列為合格。
- `IS_Kelly_pct > 0`，`實際風險_pct > 0`，`實際風險_pct <= IS_Kelly_pct + 1e-7`。
- `IS_Kelly_pct` 必須依**前四年樣本內（IS）交易**計算，不能拿後一年 OOS 訊息回看調參。原始 README 的倉位法是固定 1R、全 Kelly、半 Kelly、四分之一 Kelly；採用已實作且合格的實際風險配置，不能只因標籤寫 Kelly 就放行。

## 三、排名排序與去重

1. 對符合所有門檻的配置，先依 **`五年收益_pct` 降冪** 排序。
2. 收益相同時，依 **`最大回撤_pct` 升冪** 排序。
3. 依 `商品 + 週期 + 策略 + 出場方式` **去重**，每個唯一鍵保留上述排序的最佳合格風險配置。
4. 取前 **100** 名輸出 `Top100`；若合格配置不到 100，按真實數量輸出，不虛構補足。
5. 另輸出 **全部策略家族榜**：按五年收益降冪、最大回撤升冪，依 `原始策略族群 + 策略` 去重取最高已驗證配置。**保留不達 70 筆、低收益、負收益與缺少資料者的註記**，不得只保留獲利者；沒有合格資料的策略只能 `UNAVAILABLE/SPEC_PENDING`，不能把 0% 假裝成跑完。
6. 跨不同商品與週期的假設可能不同；必須完整顯示市場、週期、策略、出場方式、交易成本、倉位與資料驗證狀態。收益排行榜是篩選，不是實盤收益保證。
7. **OOS**（最後一年）與 IS（前四年）分開顯示，不得把 OOS 當樣本內選參；新策略歷史實作以 IS 收益／回撤選 TP 候選（0.75R/1R/1.5R/2R/3R），其偏差需明示。
8. 除主榜以外，保存可供風險比較的 `勝率`、`止損數`、`盈虧比`、`年化`、`EV`、`Sharpe`、`最大回撤`、`實際風險_pct`、`IS_Kelly_pct`、`五年交易數`、`五年收益_pct`、`OOS收益_pct`。未計算的指標標 `NOT_CALCULATED`，不得編造。

## 四、必須保留的輸出及驗收證據

每個市場×週期×family 批次保存 `ranking.csv`、`trades.csv`、`checkpoint.json`、`manifest.json`；manifest 必須包含完整五年窗、策略版本、行情來源及資料校驗、逐筆交易和排名檔案 SHA256、成功／失敗狀態。全部分數與排名必須追溯至可核驗的五年交易清單。

建議輸出：
- `top100_by_return.csv`（合格收益 Top100）
- `all_strategy_families_ranked.csv`（全部策略家族，含不合格與未驗證標記）
- `all_strategies_by_market_timeframe.csv`（每種策略、每個市場、每個週期的明細）
- `coverage.csv`（所有組合的 `COMPLETE / SKIP_RETEST / FAILED / UNAVAILABLE / SPEC_PENDING`）
- `latest_verification_manifest.json`（批次/策略組合口徑分別計數，不混計）。

**歷史數字不能混淆：** 已有 **188 個 `市場×週期×family` 批次的舊 trades/排名回放檢驗**，不是 188 個不重名策略，也**不是** 188 個在 ChatGPT 重新由五年 OHLCV 生成交易的訊號回測。原 612 分類批次中，另一 424 批次缺同層證據。應以最新完成的真正訊號測試、結果和散列另行增量記錄。

## 五、執行與程式現況

在 `research/multi-market-strategy-ranking/`：

```powershell
python -m pip install -r requirements.txt
python tools/run_legacy_all_timeframes.py --symbol BTCUSDT --timeframe 20m --family new
python tools/aggregate_all_timeframes.py
```

`run_legacy_all_timeframes.py` 是單批策略訊號測試；`aggregate_all_timeframes.py` 是**從既有來源和驗證通過的工件生成榜單**，本身不代替各組原始回測。

**需要修正的既有程式限制：** `aggregate_all_timeframes.py` 第 239–240 行硬性要求 `len(families)==38`，這是舊版 31＋7 假設，不能當成已實作了 38 種獨立策略；若最終實際對帳數不同，應先修正策略清單及相關驗證，再調整該斷言，不能造假達標。

每小時保存實際已驗證進度至 Git **`report/trade-test-multi-market-20261030`**；不動 `main`，GitHub 僅備份與版本控管，不用 Actions/Jules 代跑。

## 六、原始依據

- `tools/aggregate_all_timeframes.py`（Top100 篩選、排序、去重，約第 209–242 行）
- `research/multi-market-strategy-ranking/README.md`（倉位風控、TP、舊排名程式及執行）
- `results/combined_top100/local_python_recheck_20261030.md`（現有 Top100 已驗證/歷史快照證據）
- `results/combined_top100/TRADE_TEST_CURRENT_STATE_20261101.md`（最新要求、缺口、去重）
