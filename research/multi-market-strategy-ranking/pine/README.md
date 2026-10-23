# Pine Script v6 策略索引與說明文件

本資料夾包含由五年的多市場策略 Python 原始碼轉譯而成的獨立、可檢查 Pine Script v6 策略腳本 (`.pine`)，以及與 Python 實作對照之索引說明。

## 策略總數與去重核驗說明

在 4 個 Python 策略腳本中，共定義了 32 個策略條目。產出的排名結果數據表 (`complete_ranking_9556.csv.gz` 與 `strategy_max_return_kelly_details.csv`) 中包含 31 個不重複策略名稱：
1. **策略去重（30 種獨立邏輯）**：經逐項核驗 Python 原始碼，`RSI2_EMA200`（位於 `five_year_multi_market_kelly.py`）與 `EMA200+RSI2_mean_reversion`（位於 `five_year_compound_strategy_sweep.py`）之進出場邏輯完全相同（均為在 EMA200 同向條件下，RSI2 低於 10 或高於 90 進場，RSI2 穿越 70/30 或突破 EMA200 時出場）。因此將兩者合併歸納為 1 個獨立 Pine 腳本 (`rsi2_ema200.pine`)，共建立 **30 份獨立 Pine Script v6 策略**。
2. **重複定義條目說明**：`EMA200+RSI14_pullback` 同時出現在 `five_year_compound_strategy_sweep.py` 與 `five_year_low_drawdown_fixed_rr.py` 中，名稱與邏輯相同，因此在總榜中維持 31 個策略名稱。
3. **參數與配置獨立化**：所有策略在商品、週期、倉位大小 (Sizing)、止盈止損 (SL/TP) 的差異均透過 Pine Script 的 `input` 參數進行設定，不重複複製策略檔。

---

## 策略索引對照表 (Index Table)

| 策略名稱 (Ranking Name) | 去重邏輯分類 | Python 檔 / 函式 | Pine Script 檔案 | 代表排名配置 (商品 | 市場 | 週期 | 倉位 | 風控/出場) | TradingView / Pine 不等價注意事項 | TV 實測狀態 |
|---|---|---|---|---|---|---|
| **MACD12_26_9** | MACD (12,26,9) 雙線交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/macd12_26_9.pine`](macd12_26_9.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Supertrend+RSI50** | Supertrend(10,3) + RSI14>50 複合策略 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_rsi50.pine`](supertrend_rsi50.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Supertrend10_3** | Supertrend(10,3) 趨勢追蹤 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/supertrend10_3.pine`](supertrend10_3.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Supertrend+EMA200** | Supertrend(10,3) + EMA200 濾網 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_ema200.pine`](supertrend_ema200.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Stoch14+EMA200** | Stoch(14) 超賣/超買 + EMA200 均值回歸 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/stoch14_ema200.pine`](stoch14_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 2.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Supertrend+EMA200_flip** | Supertrend(10,3) 翻轉 + EMA200 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/supertrend_ema200_flip.pine`](supertrend_ema200_flip.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **WEMA20_50+Donchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 突破 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_donchian20.pine`](wema20_50_donchian20.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 固定4R+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異；週線指標由 request.security 取用，需留意 TradingView 重繪與 K 線對齊機制 | **未測** |
| **WEMA20_50+MACD** | 週線 EMA(20/50) + 日線 MACD 交叉 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_macd.pine`](wema20_50_macd.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: ATR移動止盈2x+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異；週線指標由 request.security 取用，需留意 TradingView 重繪與 K 線對齊機制 | **未測** |
| **EMA20_50_ADX20** | EMA(20/50) 交叉 + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/ema20_50_adx20.pine`](ema20_50_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Donchian20_10** | Donchian(20) 進場 / Donchian(10) 出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/donchian20_10.pine`](donchian20_10.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 固定1R+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **EMA50_200** | EMA(50/200) 黃金/死亡交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/ema50_200.pine`](ema50_200.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 固定1R<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **WEMA20_50+DailyDonchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_donchian20.pine`](wema20_50_daily_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異；週線指標由 request.security 取用，需留意 TradingView 重繪與 K 線對齊機制 | **未測** |
| **MACD+RSI50** | MACD 交叉 + RSI(14)>50 趨勢動能 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/macd_rsi50.pine`](macd_rsi50.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Donchian20_Volume_EMA200** | Donchian(20) + 1.5倍量能 + EMA200 濾網 | `run_strategies.py`<br>`make_state()` | [`pine/donchian20_volume_ema200.pine`](donchian20_volume_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Keltner20_1.5ATR_EMA200** | Keltner(20, 1.5ATR) 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/keltner20_15atr_ema200.pine`](keltner20_15atr_ema200.pine) | **YM=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Donchian20+ADX14** | Donchian(20) + ADX(14)>20 突破 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/donchian20_adx14.pine`](donchian20_adx14.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 1.5R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **EMA200+MACD_cross** | EMA200 方向 + MACD 交叉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_macd_cross.pine`](ema200_macd_cross.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Donchian20+MACD** | Donchian(20) 突破 + MACD 同向濾網 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/donchian20_macd.pine`](donchian20_macd.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 訊號出場(無固定TP) | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Turtle55_20_EMA200** | Turtle 55/20 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/turtle55_20_ema200.pine`](turtle55_20_ema200.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 1.5R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Bollinger20+RSI14_reentry** | 布林(20,2σ) 帶外返回 + RSI14 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/bollinger20_rsi14_reentry.pine`](bollinger20_rsi14_reentry.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Supertrend_ADX20** | Supertrend(10,3) + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/supertrend_adx20.pine`](supertrend_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **Volume_Donchian20** | 量能 1.5倍 + Donchian(20) 突破 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/volume_donchian20.pine`](volume_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 固定4R+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **RSI2_EMA200<br>*(等價: EMA200+RSI2_mean_reversion)*** | EMA200 趨勢 + RSI(2) 極端回歸 (去重邏輯) | `five_year_multi_market_kelly.py / five_year_compound_strategy_sweep.py`<br>`make_signals() / custom_signals()` | [`pine/rsi2_ema200.pine`](rsi2_ema200.pine) | **ES=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 固定1R+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **EMA200+RSI2_extreme** | EMA200 趨勢 + RSI(2)<5/95 極致反轉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_rsi2_extreme.pine`](ema200_rsi2_extreme.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **EMA200+RSI14_pullback** | EMA200 趨勢 + RSI(14) 30/70 回檔拉回 | `five_year_compound_strategy_sweep.py / five_year_low_drawdown_fixed_rr.py`<br>`custom_signals() / signals()` | [`pine/ema200_rsi14_pullback.pine`](ema200_rsi14_pullback.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **WEMA20_50+DailyMACD** | 週線 EMA(20/50) + 日線 MACD 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_macd.pine`](wema20_50_daily_macd.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異；週線指標由 request.security 取用，需留意 TradingView 重繪與 K 線對齊機制 | **未測** |
| **Bollinger20_2** | 布林通道(20,2σ) 帶外返回中軌出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/bollinger20_2.pine`](bollinger20_2.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: ATR移動止盈2x+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **MACD_EMA200_ADX20** | MACD 交叉 + EMA200 趨勢 + ADX>20 | `run_strategies.py`<br>`make_state()` | [`pine/macd_ema200_adx20.pine`](macd_ema200_adx20.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: IS選定固定TP 3R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **BB_Reentry_RSI_ADX25** | 布林返回 + RSI + ADX<25 低動能震盪 | `run_strategies.py`<br>`make_state()` | [`pine/bb_reentry_rsi_adx25.pine`](bb_reentry_rsi_adx25.pine) | **AUDUSD=X** (FX)<br>週期: 1D (日線)<br>部位: 半凱利<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |
| **RSI14_EMA200** | EMA200 趨勢 + RSI(14) 超賣/超買進場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/rsi14_ema200.pine`](rsi14_ema200.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利<br>風控: 固定2R+訊號出場 | 日線收盤確認訊號、次日開盤進場；同根 K 線觸及 SL/TP 保守假設 SL 先成交；費率與滑價模型差異 | **未測** |

---

## Python 實作與 TradingView / Pine Script 等價性與差異說明

為確保交易邏輯嚴格以 Python 原始實作爲準，以下列出 Pine Script v6 轉譯時無法完全等價之處：

1. **成交時點 (Execution Timing)**：
   - **Python 實作**：在完成的日線收盤價 (Bar Close) 確認訊號與計算 ATR，於下一根日線開盤價 (Bar Open) 以開盤價建立部位與設定初始 SL/TP。
   - **Pine Script 轉譯**：採用標準 `process_orders_on_close = false` 設定，當 K 線收盤符合條件發送 `strategy.entry` 訂單，於下一根 K 線開盤執行成交，確保訊號時點一致。

2. **同根 K 線觸及 SL/TP 優先順序 (Same-Bar Hit Order)**：
   - **Python 實作**：若同一根日線之 High/Low 同時觸及止盈 (TP) 與止損 (SL)，採保守假設，**一律視為止損 (SL) 先成交**。
   - **Pine Script 轉譯**：TradingView 歷史回測引擎對棒內 (Intrabar) 觸價順序依據 tick 資料或最高/最低價先後進行模擬，無法完全強制每筆同棒雙觸均先計算 SL，可能導致微小歷史回測差異。

3. **交易成本與滑價模型 (Costs & Slippage)**：
   - **Python 實作**：加密貨幣採 5 bps 手續費 + 5 bps 滑價；外匯採 0.4 pip/邊；傳統期貨採 1 tick/邊 + $2.5 手續費。
   - **Pine Script 轉譯**：Pine 腳本提供 `commission_type` 與 `slippage` 設定，但在不同標的（如外匯 pips 與期貨 ticks）的精確映射需於 TradingView 屬性頁面手動調校。

4. **週線指標跨時區對齊 (Weekly Indicator Resampling)**：
   - **Python 實作**：將每日 Close 重採樣至 W-SUN（每週日收盤），再計算 Weekly EMA / MACD。
   - **Pine Script 轉譯**：使用 `request.security(..., "W", ...)` 取得週線指標。由於 TradingView 週線切割時間與數據源（Yahoo Finance / Binance）可能存在微小時間差，指標數值可能有些許差異。

5. **未測標示與限制 (Execution Status)**：
   - 目前受限於沙盒環境無法連線 TradingView Pine Script 伺服器進行線上編譯與實盤驗證，**所有策略於 TradingView 實測狀態均標示為「未測」**。
   - 絕不手動估算或填寫未經 TradingView 歷史回測引擎真正執行的績效數據。
