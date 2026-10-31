# Trade Test — 2026-11-01 03:01 (+08) ETHUSDT 5m 原始 Actions 工件 SHA 驗收

## 實際執行
- 從既有 GitHub Actions run **41066783962** 下載 `market-ETHUSDT-5m`，artifact ID **12986299665**，ZIP 約 28MB，內層 `market-ETHUSDT-5m.tar.gz`。
- 在本輪本地 Python 用 `zipfile` + `tarfile` + `hashlib.sha256` **逐一讀取四個 family 的原始 ranking.csv、trades.csv、manifest.json**，不是僅檢查 artifact metadata。
- 四個 manifest 均 `status=complete`；歷史 2021-10-10T00:00Z 至 2026-10-10T00:00Z（exclusive）；各報告 525888 根 5m K、0 個 missing/irregular intervals；四個宣告的 OHLCV SHA 一致 `fc230732cd7d7b6756e5b8cc4dbaf44ed6f54ef710a3fc5304b05fcfde8851bc`。
- 本輪未取得原始 K 棒檔案，故 **OHLCV SHA 只是 manifest 宣告，並未獨立重算**。CSV SHA 則確實從工件位元組重新計算通過。

| family | ranking.csv SHA256 | trades.csv SHA256 | CSV hash verified |
|---|---|---|---|
| original | `41faf118ea149b5cafed814b46cac46b5a4d215781ce8441b3325e64751efdd2` | `758116466ef2256f2f0eadb380804388a0bab1a91e0cea26f08e9d8fd4a72a22` | yes |
| compound | `8daa619c89012798c080a4dd9d13ab9d9f7b4ce798691b78075f96e99e5d5f76` | `d1d0bf82f620a11af219c0fc74b073798fa25430b1e6c195c8e296e601925353` | yes |
| fixed | `cc55ba0a1aa88869fe3f76f2ce8d74a4878aa1e4f2846f7ef1f4d4b99481b63f` | `4baa4c747afee4929268bc61fe87d1b1dd744ee5ab1f38c595802e014a33745e` | yes |
| new | `6ccb559f6c276ce541b9b732ca68820f9642a0e885c372a2b3b32e5899f3f8a6` | `ff81961d7c57b33ffb94b8eab17e7daa316f29c77966c8c25121c82a68dda925` | yes |

## 本輪完成口徑
- 新跑出五年 OHLCV **策略訊號組合：0**。
- 已存在完整五年訊號結果、此次首次獨立讀取並核對交易及排名 CSV SHA：**ETHUSDT 5m 四個 family**。不得與舊 124／138 批直接相加；須先用 `market×timeframe×family×strategy×exit` 去重。
- 這是舊工件完整性驗算，不是交易回放，也不是新 OHLCV 訊號回測。
- 既有總清單仍標示 124/612 已驗成交回放，另有前輪 138 個去重 SHA 完整工件，兩者驗收口徑不同；不能宣稱已完成 612。
- 不重跑舊 1d；不重跑本輪 ETH 5m 四個完整工件。未修改雙榜：無新的合格績效、IS Kelly/伯努利 iid 仍無新驗證。完整 38 家族榜及 Kelly Top100 仍採 `local_python_38_families_20261030.csv`、`local_python_kelly_top100_20261030.csv`。
- 需後續下載 ETH 1m/3m 的原始工件、完成 SHA；若可取得原始 OHLCV 則以實際 Python 回測真正未完成的 20m 等缺口。非加密 5 年分鐘 OHLCV 不可用仍標 `unavailable`。
- 不交 Jules，不新增 workflow，不動 main。
