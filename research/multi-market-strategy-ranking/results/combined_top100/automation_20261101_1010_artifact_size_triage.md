# Trade Test — 2026-11-01 10:10 +08 — 實際 Python 庫存核驗與工件大小異常排查

## 本輪可重現的 Python 執行
使用 Python 3 的 csv.DictReader、collections.Counter、hashlib.sha256 讀取本地 `trade_test_run6_local_sha_inventory.csv`：
- 檔案 SHA256：`3ec2575d8122c58788f4ae248981649683f2ac316dcc813348cb3f805e3d5ebf`；138 列。
- 欄位僅 `symbol,timeframe,family,complete_and_sha,ranking_rows,trade_rows,source`，缺少 strategy、exit、OHLCV SHA，故不能據此認定逐策略訊號回測完成。
- family：fixed 37、compound 36、original 36、new 29；市場：BTC 38、ETH 48、SOL 36、GC 4、SI 4、ES 4、NQ 4。
- 20m 0 筆，僅限本地 CSV 庫存。
- 本輪新產生五年原始 OHLCV 策略訊號：**0 組**；新交易回放驗算：**0 組**；新工件內容 SHA 驗證：**0 組**。

## GitHub Actions #41066783962 工件 metadata 新查核
直接讀取 GitHub API `/repos/tofueu/trade-test/actions/runs/41066783962/artifacts?per_page=100`，31 個 artifacts。
- ETH 1m id 12993586056，151493344 bytes，ZIP digest `sha256:507ac6862784d2ea73dafa04b76d7aca86b984ee49b61f39128ea78d80885f31`。
- ETH 3m id 12988929734，49106611 bytes，ZIP digest `sha256:a53868d60ad92fb3711f66da0b446ea3a2a2f03b4b3eb55954533d2185cb34a1`。
- ETH 5m id 12986299665，28902635 bytes，ZIP digest `sha256:2039fd39c0b82ce4da8a2aa4f94cf9e800f02d6ea9930adf2b924d40f7f27ae6`。
- 重要異常：同一 run 的 SOL 3m、1h、30m、1d、2h 工件僅 293–297 bytes；^TWII 1d 287 bytes、USDJPY=X 1d 296 bytes。**這些很可能是狀態/錯誤檔，不能因為 artifact 存在就標記 complete**。須下載內文判定，不可單憑大小斷言失敗或 unavailable。
- 以上 digest 是 GitHub 提供的外層 ZIP metadata，**不是本輪獨立下載重算的 SHA，也不是原始 OHLCV SHA**。metadata 皆顯示未過期，期限至 2026-11-29。

## 後續必要的實際修復
1. 先讀取小型 artifacts 內容以分辨失敗、資料缺口、空結果；不重跑已有 complete + 獨立驗證的批次。
2. 取得 ETH 1m/3m ZIP 並以 Python 逐檔驗證內層 manifest/rankings/trades SHA；與 K 線 SHA 分欄。
3. 從五年連續真實 5m OHLCV 按四根組成 20m，檢查缺口，再只跑未完成的策略×出場。
4. 逐筆交易與 strategy/exit 鍵缺失前，completed/required 尚不可計算。舊 31 種 1d 不重測。兩份歷史榜不覆蓋，正式 Top100 必須重新驗五年、>=70 筆、收益 >100%、risk<=IS Kelly；iid 不宣稱已驗證。

未修改 main、未新增 workflow、未交 Jules。