# ETHUSDT 3h 五年 Python 策略工件增量稽核 — 2026-10-31

來源：GitHub Actions Run [41068912974](https://github.com/tofueu/trade-test/actions/runs/41068912974) 的 `market-ETHUSDT-3h`，artifact ID **13009351170**，從 GitHub 下載 ZIP 後在 Python 中開啟內層 `market-ETHUSDT-3h.tar.gz`。

## 本輪實際檢查結果

- 原始五年窗口：`2021-10-10T00:00:00+00:00` 至 `2026-10-10T00:00:00+00:00`（end-exclusive）。
- ETHUSDT 3h 共 **14,608** 根 K 線；四分類 `missing_or_irregular_intervals=0`；同一來源 `OHLCV_SHA256=1c1f0c3119ef8766de10c2f4c86ddcae1d91f2e4e883d19c7a34af9284a9db3d`。
- **original**：8 策略、288 排名列、30,942 筆儲存成交；`manifest.status=complete`；`ranking_sha256` 和 `trades_sha256` 均與實際檔案 SHA256 相符。
- **compound**：8 策略、32 排名列、4,419 筆儲存成交；`status=complete`；兩個 SHA256 均相符。
- **fixed**：9 策略、36 排名列、3,419 筆儲存成交；`status=complete`；兩個 SHA256 均相符。
- **new**：7 策略、28 排名列、1,679 筆儲存成交；`status=complete`；兩個 SHA256 均相符。
- 合計 **384 排名列、40,459 筆保存成交**，**4/4 分類 SHA256 完整相符**。此為實際 Python 檢查下載的完整工件，不是只看 Actions job success。
- `ranking.csv` 有多個風險配置，`trades.csv` 是策略/出場的交易 R 記錄，**不能以每列 ranking 的五年交易數直接等同 trades.csv 中該策略/出場的所有交易列數**；本輪未獨立重算全部 Kelly 淨值路徑。
- 既有去重清單把 `ETHUSDT,3h` 四類都標成 `PENDING_FULL_FIVE_YEAR_PYTHON`，應在下次增量合併時改為「已取得完整五年工件，SHA 驗證通過」，**不應重跑 ETH 3h 訊號**。更新正式 `SKIP_RETEST` 清單前需同步來源 artifact ID、檢查方法與原始排名合併去重，避免覆蓋現有 124 批獨立成交回放基準。
- 此次新增的是 **4 個已下載並驗 SHA 的完整五年策略執行分類**；不是重新跑四次 OHLCV 策略訊號，也不是已經完成全部 612 個批次。不得把 4 批直接加到原 124 個「SHA + 獨立成交 R 回放」嚴格驗收口徑，兩種驗證層級須分開計數。

不交 Jules、不動 main、不新增 workflow。未完成項目仍須補齊真實行情與缺漏策略碼。
