# Pine Script v6 策略索引與說明文件

本資料夾包含由五年的多市場策略 Python 原始碼轉譯而成的獨立、可檢查 Pine Script v6 策略腳本 (`.pine`)，以及與 Python 實作對照之索引說明。

## 策略總數與去重核驗說明

在 4 個 Python 策略腳本中，共定義了 32 個策略條目。產出的排名結果數據表 (`complete_ranking_9556.csv.gz` 與 `strategy_max_return_kelly_details.csv`) 中包含 31 個不重複策略名稱：
1. **策略去重（30 種獨立邏輯）**：經逐項核驗 Python 原始碼，`RSI2_EMA200`（位於 `five_year_multi_market_kelly.py`）與 `EMA200+RSI2_mean_reversion`（位於 `five_year_compound_strategy_sweep.py`）之進出場邏輯完全相同。因此將兩者合併歸納為 1 個獨立 Pine 腳本 (`rsi2_ema200.pine`)，共建立 **30 份獨立 Pine Script v6 策略**。
2. **重複定義條目說明**：`EMA200+RSI14_pullback` 在排名數據中同時涵蓋 Pure Fixed-RR 版本與 Compound Signal Exit 版本，Pine 腳本 (`ema200_rsi14_pullback.pine`) 透過 `exit_mode` 參數提供兩種出場模式切換，完全覆蓋兩種 Python 實作變體。
3. **參數與配置獨立化**：所有策略在商品、週期、倉位大小 (Sizing)、止盈止損 (SL/TP) 的差異均透過 Pine Script 的 `input` 參數進行設定，不重複複製策略檔。

---

## 策略索引對照表 (Index Table)

| 策略名稱 (Ranking Name) | 去重邏輯分類 | Python 檔 / 函式 | Pine Script 檔案 | 代表排名配置 (商品 | 市場 | 週期 | 倉位 | 風控/出場) | Cost & Engine 注意事項 | TV 實測狀態 |
|---|---|---|---|---|---|---|
| **MACD12_26_9** | MACD (12,26,9) 雙線交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/macd12_26_9.pine`](macd12_26_9.pine) | **XRPUSDT** (Crypto futures)<br>排名代表週期: 1D (日線)<br>Pine訊號週期: 留白=圖表週期；或選同級/較高週期<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Supertrend+RSI50** | Supertrend(10,3) + RSI14>50 複合策略 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_rsi50.pine`](supertrend_rsi50.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Supertrend10_3** | Supertrend(10,3) 趨勢追蹤 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/supertrend10_3.pine`](supertrend10_3.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.5%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Supertrend+EMA200** | Python Supertrend(ATR10 EWM, 3) + EMA200 對齊持倉；訊號失配即退出 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()`；指標：`five_year_multi_market_kelly.py / indicators()` | [`pine/supertrend_ema200.pine`](supertrend_ema200.pine) | **SOLUSDT** (Crypto futures)<br>榜單基準週期: 1D；程式按目前圖表週期計算，可切換 4H/1H/15m/5m/1m<br>全凱利 (IS Kelly: 23.5371%)<br>ATR14 × 1.5 初始 SL，無固定 TP | EWM/訊號規則已按 Python 對照；每邊總成本以 0.10% Pine commission 近似 Python 0.05% fee + 0.05% slippage；圖表週期切換結果另屬新配置 | **TV 未測** |
| **Stoch14+EMA200** | Stoch(14) 超賣/超買 + EMA200 均值回歸 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/stoch14_ema200.pine`](stoch14_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.9%)<br>風控: 純固定TP 2.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **Supertrend+EMA200_flip** | Supertrend(10,3) 翻轉 + EMA200 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/supertrend_ema200_flip.pine`](supertrend_ema200_flip.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (44.4%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **WEMA20_50+Donchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 突破 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_donchian20.pine`](wema20_50_donchian20.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (46.0%)<br>風控: 固定4R+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價；週線 request.security[1] (lookahead_on) | **未測** |
| **WEMA20_50+MACD** | 週線 EMA(20/50) + 日線 MACD 交叉 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_macd.pine`](wema20_50_macd.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (26.5%)<br>風控: ATR移動止盈2x+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價；週線 request.security[1] (lookahead_on) | **未測** |
| **EMA20_50_ADX20** | EMA(20/50) 交叉 + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/ema20_50_adx20.pine`](ema20_50_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (77.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Donchian20_10** | Donchian(20) 進場 / Donchian(10) 出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/donchian20_10.pine`](donchian20_10.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.8%)<br>風控: 固定1R+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **EMA50_200** | EMA(50/200) 黃金/死亡交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/ema50_200.pine`](ema50_200.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 固定1R (0.0%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **WEMA20_50+DailyDonchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_donchian20.pine`](wema20_50_daily_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價；週線 request.security[1] (lookahead_on) | **未測** |
| **MACD+RSI50** | MACD 交叉 + RSI(14)>50 趨勢動能 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/macd_rsi50.pine`](macd_rsi50.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (10.5%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Donchian20_Volume_EMA200** | Donchian(20) + 1.5倍量能 + EMA200 濾網 | `run_strategies.py`<br>`make_state()` | [`pine/donchian20_volume_ema200.pine`](donchian20_volume_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (63.5%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **Keltner20_1.5ATR_EMA200** | Keltner(20, 1.5ATR) 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/keltner20_15atr_ema200.pine`](keltner20_15atr_ema200.pine) | **YM=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (47.2%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **Donchian20+ADX14** | Donchian20+ADX14 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/donchian20_adx14.pine`](donchian20_adx14.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.3%)<br>風控: 純固定TP 1.5R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **EMA200+MACD_cross** | EMA200 方向 + MACD 交叉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_macd_cross.pine`](ema200_macd_cross.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **Donchian20+MACD** | Donchian20+MACD | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/donchian20_macd.pine`](donchian20_macd.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (21.6%)<br>風控: 訊號出場(無固定TP) | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Turtle55_20_EMA200** | Turtle 55/20 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/turtle55_20_ema200.pine`](turtle55_20_ema200.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (34.3%)<br>風控: IS選定固定TP 1.5R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Bollinger20+RSI14_reentry** | 布林(20,2σ) 帶外返回 + RSI14 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/bollinger20_rsi14_reentry.pine`](bollinger20_rsi14_reentry.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (17.8%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Supertrend_ADX20** | Supertrend(10,3) + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/supertrend_adx20.pine`](supertrend_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (40.6%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **Volume_Donchian20** | 量能 1.5倍 + Donchian(20) 突破 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/volume_donchian20.pine`](volume_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (27.7%)<br>風控: 固定4R+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **RSI2_EMA200<br>*(等價: EMA200+RSI2_mean_reversion)*** | EMA200 趨勢 + RSI(2) 極端回歸 (去重邏輯) | `five_year_multi_market_kelly.py / five_year_compound_strategy_sweep.py`<br>`make_signals() / custom_signals()` | [`pine/rsi2_ema200.pine`](rsi2_ema200.pine) | **ES=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (30.9%)<br>風控: 固定1R+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **EMA200+RSI2_extreme** | EMA200 趨勢 + RSI(2)<5/95 極致反轉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_rsi2_extreme.pine`](ema200_rsi2_extreme.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (13.5%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **EMA200+RSI14_pullback** | EMA200 趨勢 + RSI(14) 30/70 回檔拉回 | `five_year_compound_strategy_sweep.py / five_year_low_drawdown_fixed_rr.py`<br>`custom_signals() / signals()` | [`pine/ema200_rsi14_pullback.pine`](ema200_rsi14_pullback.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (55.3%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **WEMA20_50+DailyMACD** | 週線 EMA(20/50) + 日線 MACD 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_macd.pine`](wema20_50_daily_macd.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.7%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價)；週線 request.security[1] (lookahead_on) | **未測** |
| **Bollinger20_2** | 布林通道(20,2σ) 帶外返回中軌出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/bollinger20_2.pine`](bollinger20_2.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.1%)<br>風控: ATR移動止盈2x+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: $2.50/口 + 1 tick滑價 | **未測** |
| **MACD_EMA200_ADX20** | MACD 交叉 + EMA200 趨勢 + ADX>20 | `run_strategies.py`<br>`make_state()` | [`pine/macd_ema200_adx20.pine`](macd_ema200_adx20.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (15.1%)<br>風控: IS選定固定TP 3R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |
| **BB_Reentry_RSI_ADX25** | 布林返回 + RSI + ADX<25 低動能震盪 | `run_strategies.py`<br>`make_state()` | [`pine/bb_reentry_rsi_adx25.pine`](bb_reentry_rsi_adx25.pine) | **AUDUSD=X** (FX)<br>週期: 1D (日線)<br>部位: 半凱利 (31.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.4 pips 滑價 | **未測** |
| **RSI14_EMA200** | EMA200 趨勢 + RSI(14) 超賣/超買進場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/rsi14_ema200.pine`](rsi14_ema200.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (23.8%)<br>風控: 固定2R+訊號出場 | calc_on_order_fills=false 無前瞻預裝 SL；pointvalue 下單量校正；費率: 0.10% (5bps費+5bps滑價) | **未測** |

---

## 第一名策略的圖表／選擇週期設定

- `macd12_26_9.pine` 新增「Signal timeframe」輸入；留白時跟隨圖表週期，例如圖表切至 4 小時即以 4 小時 MACD(12,26,9) 與 ATR(14) 計算。也可選擇等於或高於圖表的訊號週期。
- 為避免高週期未收盤資料造成重繪，選擇高於圖表的週期時，只使用已確認的高週期訊號，並在新高週期開始後第一根圖表 K 棒收盤時判斷，再於下一根圖表 K 棒開盤送出市價單。這會比原 Python「下一根訊號週期開盤」晚最多一根圖表 K 棒；屬於 Pine 執行模型差異。
- 不接受低於圖表週期、或不能整數對齊的週期組合。要用 1 小時訊號，請把圖表也設為 1 小時或更低。
- 訊號、ATR 止損、止盈與倉位公式未改；仍保留 20.067% 初始資金風險率與 1.5 ATR 初始止損。Pine v6 預設 100% 保證金下，較小 ATR 算出的名目部位可能超過本金而被模擬器拒單。未經確認不調整槓桿、保證金或部位上限。
- 這項週期選擇修改尚未在 Pine 編譯器或 TradingView 實測；此策略仍標示「未測」。

---

## Python 實作與 TradingView / Pine Script 平台差異與限制說明

依據 PR 審查意見（Comments #6362723774, #6363140734, #6363214309, #6365371345, #6366183824, #6366889661, #6367049157, #6367472891, #6367965217, #6380908626），本專案轉譯之 30 份 Pine 腳本已做出以下精確對齊與限制說明：

1. **無前瞻性防護止損預裝 (`calc_on_order_fills=false`)**：
   - 全 30 份 Pine 腳本將 `calc_on_order_fills` 設定為 `false`。訊號棒收盤時，腳本以該棒已完成的 ATR 計算 `loss`／`profit` tick 距離，並與 `strategy.entry` 同時提交保護單；TradingView 以實際成交價為基準計算相對 tick 距離，避免跳空時把止損錯錨在前一棒收盤價。距離會依商品最小跳動單位取整，與 Python 的連續價格距離可能相差最多約半個 tick。持倉後的固定止損則在後續計算中以成交價及前一棒 ATR 重錨；因未啟用成交後立即重算，成交棒內的成交順序與 Python 逐棒引擎仍需在 TradingView 實測確認，不宣稱完全等價。所有腳本仍標示「未測」。

2. **Target-State 轉換門控與雙變體支援 (Target-State Gating & Dual Variant Support)**：
   - **持續狀態策略 (21 Persistent State Strategies)**：追蹤目標部位狀態 `target_state in {-1, 0, 1}`，僅在 `target_state` 改變時觸發建倉，並保持該狀態直到 Python 出場條件成立 (`target_state := 0`)。當反轉訊號出現時可於同一開盤價執行反轉建倉，若發生訊號出場則使用 `strategy.cancel()` 撤銷舊止損單優先執行訊號平倉/反轉。
   - **純固定盈虧事件策略 (9 Pure Fixed-RR Event Strategies)**：如 `five_year_low_drawdown_fixed_rr.py` 之事件型策略，要求 `strategy.position_size == 0` 方可於新事件觸發時建倉。
   - **`EMA200+RSI14_pullback.pine`**：提供 `exit_mode` 選擇參數，完全覆蓋 `five_year_low_drawdown_fixed_rr.py`（Pure Fixed-RR 模式）與 `five_year_compound_strategy_sweep.py`（Compound Signal Exit 模式）兩種 Python 實作變體。

3. **期貨點值與部位 Sizing 校正 (Point-Value Contract Sizing Multiplier)**：
   - **Python 實作**：`fixed_risk_stats()` 美元風險金額 $R = 10,000 	imes 	ext{risk\_pct}$，下單張數 $N = R / 	ext{SL\_dist}$。
   - **Pine Script 對齊**：TradingView 期貨合約每點價值為 `syminfo.pointvalue`（如 ES 為 $50, NQ 為 $20, GC 為 $100）。全 30 份 Pine 腳本均將單口風險計算為 `risk_per_contract = dist * syminfo.pointvalue`，確保期貨下單張數正確匹配設定之美元風險金額。

4. **環境限制與「未測」標示 (Environment Limitations & Execution Status)**：
   - 沙盒環境未包含原生 Pine Script v6 編譯器或 TradingView 線上回測執行連線。因此，**所有 30 份 Pine 策略於 TradingView 實測狀態均標示為「未測」**，絕不手動估算或填寫未經 TradingView 歷史回測引擎真正執行的績效數據。


---

## 另行獨立研究項目標示 (Pending Strategy Research Item)

* **項目名稱**：15 分鐘 RSI 與 5 分鐘均線組合策略 (15-minute RSI + 5-minute MA strategy combination)
* **當前狀態**：`SPEC_PENDING`（缺少完整規格說明）
* **缺少之規格參數**：
  1. 進場條件與跨時間週期對齊規則（5m MA 交叉與 15m RSI 閾值之具體判定邏輯）。
  2. 出場機制（訊號出場、指標反轉或固定盈虧倍數）。
  3. 風控與止盈止損參數（初始 SL 之 ATR 倍數與 TP 之 R 倍數）。
  4. 倉位大小與風險比率（Initial Capital 風險百分比或凱利比率）。
  5. 歷史行情數據源與商品清單（Binance/Yahoo 5m/15m K 線資料彙整）。
* **說明**：依據指導原則，本專案不自行捏造交易規則或將未定義策略混入現有 30 份 Pine 腳本中，維持 `SPEC_PENDING` 狀態等待完整規格確立。
