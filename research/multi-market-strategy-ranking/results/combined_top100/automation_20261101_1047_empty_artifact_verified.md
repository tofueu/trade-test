# Trade Test — 2026-11-01 10:47 +08 — 空工件內容驗證

## 本輪新增可核實結果
實際下載 GitHub Actions run #41066783962 的 4 份 ZIP，使用 Python zipfile、tarfile、hashlib.file_digest 逐層解包並獨立計算 ZIP SHA256。4/4 外層 ZIP SHA 與 GitHub digest 一致；4/4 內層 tar.gz 僅含**空目錄**（非檔案，size=0），沒有 manifest.json、rankings CSV、trades CSV，**不得計為任何完成策略訊號回測**。

| 市場/時區 | artifact ID | ZIP SHA256 | TAR 內容 |
|---|---:|---|---|
| SOLUSDT 3m | 12985660219 | fe3959b35a0060782ca5628088ac7fe0507c91f27e72724963377a926ccea6e9 | multi_SOLUSDT_3m_original 空目錄 |
| SOLUSDT 5m | 12984004347 | b023cd7d1c1ce9bd6e78a613f9a7a9dd1c472b585c3873361f7cf1ba217e1220 | multi_SOLUSDT_5m_original 空目錄 |
| ^TWII 1d | 12985281011 | 388d37d7a2f0f67b7033e99294717b18a54886f50b24d6d4d9643e3623b77118 | multi_^TWII_1d_original 空目錄 |
| USDJPY=X 1d | 12984539235 | 51a72019bae29f3dae63bc9b3af476a5ce7434fdccc145c28fc254fa2d2dca16 | multi_USDJPY=X_1d_original 空目錄 |

另外完整列舉 run #41066783962 的 31 個 artifacts：**14 個小於 1000 bytes**（12 個 SOLUSDT、^TWII 1d、USDJPY=X 1d），而非前輪僅列出的 7 個。其餘 10 個小工件尚未逐一解包，不能直接判定內容相同。這些空工件是輸出缺失的直接證據，但尚不能推定是資料源、runner 還是策略程式造成；須檢查既有 job logs 和 OHLCV 缺口，不能盲目重跑。舊 1d 已完成的歷史基準不重跑，空工件不覆蓋舊基準。

## 完成口徑與下一步
本輪**新跑出五年真實 OHLCV 策略訊號：0 組**；舊交易回放驗算：0 組；**新增獨立 ZIP SHA256 驗證：4 個**；內層策略 manifest/trades SHA：0 組。138 個本地 family 級工件和 124/612 舊回放仍不能直接換算逐策略完成率。先排除空工件，再收取 BTC 1m original/compound、ETH 1m/3m；只有取得五年真實 OHLCV 才補跑 20m（4 根連續 5m），不造價、不重跑已完成配置。38 家族歷史榜及 Top100 保留，不把未經逐筆 Kelly 與 iid 驗證的歷史排名稱為新完成結果。

本輪未修改 main、未交 Jules、未新增 workflow。
