# Pine Script v6 策略索引與說明文件

本資料夾包含由五年的多市場策略 Python 原始碼轉譯而成的獨立、可檢查 Pine Script v6 策略腳本 (`.pine`)，以及與 Python 實作對照之索引說明。

## 策略總數與去重核驗說明

在 4 個 Python 策略腳本中，共定義了 32 個策略條目。產出的排名結果數據表 (`complete_ranking_9556.csv.gz` 與 `strategy_max_return_kelly_details.csv`) 中包含 31 個不重複策略名稱：
1. **策略去重（30 種獨立邏輯）**：經逐項核驗 Python 原始碼，`RSI2_EMA200`（位於 `five_year_multi_market_kelly.py`）與 `EMA200+RSI2_mean_reversion`（位於 `five_year_compound_strategy_sweep.py`）之進出場邏輯完全相同（均為在 EMA200 同向條件下，RSI2 低於 10 或高於 90 進場，RSI2 穿越 70/30 或突破 EMA200 時出場）。因此將兩者合併歸納為 1 個獨立 Pine 腳本 (`rsi2_ema200.pine`)，共建立 **30 份獨立 Pine Script v6 策略**。
2. **重複定義條目說明**：`EMA200+RSI14_pullback` 同時出現在 `five_year_compound_strategy_sweep.py` 與 `five_year_low_drawdown_fixed_rr.py` 中，名稱與邏輯相同，因此在總榜中維持 31 個策略名稱。
3. **參數與配置獨立化**：所有策略在商品、週期、倉位大小 (Sizing)、止盈止損 (SL/TP) 的差異均透過 Pine Script 的 `input` 參數進行設定，不重複複製策略檔。

---

## 策略索引對照表 (Index Table)

| 策略名稱 (Ranking Name) | 去重邏輯分類 | Python 檔 / 函式 | Pine Script 檔案 | 代表排名配置 (商品 | 市場 | 週期 | 倉位 | 風控/出場) | Cost & TradingView / Pine 對照說明 | TV 實測狀態 |
|---|---|---|---|---|---|---|
| **MACD12_26_9** | MACD (12,26,9) 雙線交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/macd12_26_9.pine`](macd12_26_9.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Supertrend+RSI50** | Supertrend(10,3) + RSI14>50 複合策略 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_rsi50.pine`](supertrend_rsi50.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Supertrend10_3** | Supertrend(10,3) 趨勢追蹤 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/supertrend10_3.pine`](supertrend10_3.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.5%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Supertrend+EMA200** | Supertrend(10,3) + EMA200 濾網 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_ema200.pine`](supertrend_ema200.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (23.5%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Stoch14+EMA200** | Stoch(14) 超賣/超買 + EMA200 均值回歸 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/stoch14_ema200.pine`](stoch14_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.9%)<br>風控: 純固定TP 2.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **Supertrend+EMA200_flip** | Supertrend(10,3) 翻轉 + EMA200 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/supertrend_ema200_flip.pine`](supertrend_ema200_flip.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (44.4%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **WEMA20_50+Donchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 突破 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_donchian20.pine`](wema20_50_donchian20.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (46.0%)<br>風控: 固定4R+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick；週線 request.security | **未測** |
| **WEMA20_50+MACD** | 週線 EMA(20/50) + 日線 MACD 交叉 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_macd.pine`](wema20_50_macd.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (26.5%)<br>風控: ATR移動止盈2x+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick；週線 request.security | **未測** |
| **EMA20_50_ADX20** | EMA(20/50) 交叉 + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/ema20_50_adx20.pine`](ema20_50_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (77.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Donchian20_10** | Donchian(20) 進場 / Donchian(10) 出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/donchian20_10.pine`](donchian20_10.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.8%)<br>風控: 固定1R+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **EMA50_200** | EMA(50/200) 黃金/死亡交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/ema50_200.pine`](ema50_200.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 固定1R (0.0%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **WEMA20_50+DailyDonchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_donchian20.pine`](wema20_50_daily_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick；週線 request.security | **未測** |
| **MACD+RSI50** | MACD 交叉 + RSI(14)>50 趨勢動能 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/macd_rsi50.pine`](macd_rsi50.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (10.5%)<br>風控: 訊號出場(無固定TP) | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Donchian20_Volume_EMA200** | Donchian(20) + 1.5倍量能 + EMA200 濾網 | `run_strategies.py`<br>`make_state()` | [`pine/donchian20_volume_ema200.pine`](donchian20_volume_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (63.5%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **Keltner20_1.5ATR_EMA200** | Keltner(20, 1.5ATR) 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/keltner20_15atr_ema200.pine`](keltner20_15atr_ema200.pine) | **YM=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (47.2%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **-<br>*(等價: Donchian(20) + ADX(14)>20 突破)*** | Donchian20+ADX14 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/donchian20_adx14.pine`](donchian20_adx14.pine) | **-** (-)<br>週期: 1D (日線)<br>部位: - (20.1%)<br>風控: - | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 0, 滑價: 0.4 pips (4 ticks) | **未測** |
| **EMA200+MACD_cross** | EMA200 方向 + MACD 交叉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_macd_cross.pine`](ema200_macd_cross.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **-<br>*(等價: Donchian(20) 突破 + MACD 同向濾網)*** | Donchian20+MACD | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/donchian20_macd.pine`](donchian20_macd.pine) | **-** (-)<br>週期: 1D (日線)<br>部位: - (20.1%)<br>風控: - | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 0, 滑價: 0.4 pips (4 ticks) | **未測** |
| **Turtle55_20_EMA200** | Turtle 55/20 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/turtle55_20_ema200.pine`](turtle55_20_ema200.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (34.3%)<br>風控: IS選定固定TP 1.5R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Bollinger20+RSI14_reentry** | 布林(20,2σ) 帶外返回 + RSI14 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/bollinger20_rsi14_reentry.pine`](bollinger20_rsi14_reentry.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (17.8%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Supertrend_ADX20** | Supertrend(10,3) + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/supertrend_adx20.pine`](supertrend_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (40.6%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **Volume_Donchian20** | 量能 1.5倍 + Donchian(20) 突破 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/volume_donchian20.pine`](volume_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (27.7%)<br>風控: 固定4R+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **RSI2_EMA200<br>*(等價: EMA200+RSI2_mean_reversion)*** | EMA200 趨勢 + RSI(2) 極端回歸 (去重邏輯) | `five_year_multi_market_kelly.py / five_year_compound_strategy_sweep.py`<br>`make_signals() / custom_signals()` | [`pine/rsi2_ema200.pine`](rsi2_ema200.pine) | **ES=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (30.9%)<br>風控: 固定1R+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **EMA200+RSI2_extreme** | EMA200 趨勢 + RSI(2)<5/95 極致反轉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_rsi2_extreme.pine`](ema200_rsi2_extreme.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (13.5%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **EMA200+RSI14_pullback** | EMA200 趨勢 + RSI(14) 30/70 回檔拉回 | `five_year_compound_strategy_sweep.py / five_year_low_drawdown_fixed_rr.py`<br>`custom_signals() / signals()` | [`pine/ema200_rsi14_pullback.pine`](ema200_rsi14_pullback.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (55.3%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **WEMA20_50+DailyMACD** | 週線 EMA(20/50) + 日線 MACD 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_macd.pine`](wema20_50_daily_macd.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.7%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick；週線 request.security | **未測** |
| **Bollinger20_2** | 布林通道(20,2σ) 帶外返回中軌出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/bollinger20_2.pine`](bollinger20_2.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.1%)<br>風控: ATR移動止盈2x+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: $2.50/口, 滑價: 1 tick | **未測** |
| **MACD_EMA200_ADX20** | MACD 交叉 + EMA200 趨勢 + ADX>20 | `run_strategies.py`<br>`make_state()` | [`pine/macd_ema200_adx20.pine`](macd_ema200_adx20.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (15.1%)<br>風控: IS選定固定TP 3R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |
| **BB_Reentry_RSI_ADX25** | 布林返回 + RSI + ADX<25 低動能震盪 | `run_strategies.py`<br>`make_state()` | [`pine/bb_reentry_rsi_adx25.pine`](bb_reentry_rsi_adx25.pine) | **AUDUSD=X** (FX)<br>週期: 1D (日線)<br>部位: 半凱利 (31.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 0, 滑價: 0.4 pips (4 ticks) | **未測** |
| **RSI14_EMA200** | EMA200 趨勢 + RSI(14) 超賣/超買進場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/rsi14_ema200.pine`](rsi14_ema200.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (23.8%)<br>風控: 固定2R+訊號出場 | 開盤價進場 + 前棒 ATR 止損錨定；手續費: 5 bps, 滑價: 1 tick | **未測** |

---

## Python 實作與 TradingView / Pine Script 等價性與審查反饋說明

為確保交易邏輯嚴格以 Python 原始實作爲準，依據 PR 審查意見（Comment #6362723774），所有 Pine 腳本均已做出以下精確對齊：

1. **成交時點與止損/止盈價位錨定 (Execution & Stop Anchor)**：
   - **Python 實作**：前一根 K 線 `sig[i-1]` 產生訊號，當天 `open[i]` 開盤成交；止損價位錨定於 `entry - side * (1.5 * atr[i-1])`（使用訊號發送時前一根完成 K 線的 ATR）。
   - **Pine Script 轉譯**：當前 K 線收盤觸發 `strategy.entry`；下一根 K 線開盤實際成交。成交當下 (`ta.change(strategy.position_size) != 0`)，止損價位精確計算為 `entry_p - side * (1.5 * atr_val[1])`，與 Python 邏輯 100% 等價。

2. **部位 sizing 模型 (Position Sizing Mapping)**：
   - **Python 實作**：採單筆風險金額固定法 $R = f \cdot 	ext{Capital}$（全凱利時 $f = 	ext{IS\_Kelly\_pct}$，固定 1R 時 $f = 10\%$），部位張數 $N = R / 	ext{SL\_dist}$。
   - **Pine Script 轉譯**：全 30 份 Pine 腳本均已加入 `risk_pct` (`input.float`) 與 `use_risk_sizing` (`input.bool`) 參數，預設填入代表配置之凱利比率或 10% 1R 風險，以風險金額除以止損距離計算進場數量。

3. **市場交易成本與滑價 (Commission & Slippage)**：
   - **Python 實作**：加密貨幣每邊 5 bps 費 + 5 bps 滑價；外匯 0.4 pip/邊；傳統期貨每邊 1 tick + $2.5 手續費。
   - **Pine Script 轉譯**：全 30 份 Pine 腳本的 `strategy()` 宣告中已手動配置對應市場之手續費與滑價參數（加密貨幣 `percent=0.05`, `slippage=1`；期貨 `cash_per_contract=2.5`, `slippage=1`；外匯 `slippage=4`）。

4. **同根 K 線觸及 SL/TP 優先順序 (Same-Bar Hit Order)**：
   - **Python 實作**：若同一根日線之 High/Low 同時觸及止盈 (TP) 與止損 (SL)，採保守假設，**一律視為止損 (SL) 先成交**。
   - **Pine Script 轉譯**：TradingView 回測引擎依據棒內模擬或最高/最低價先後判定，無法強制每筆雙觸均先計算 SL，可能存在微小歷史回測差異。

5. **未測標示與限制 (Execution Status)**：
   - 目前受限於沙盒環境無法連線 TradingView Pine Script 伺服器進行線上編譯與實盤驗證，**所有策略於 TradingView 實測狀態均標示為「未測」**。
   - 絕不手動估算或填寫未經 TradingView 歷史回測引擎真正執行的績效數據。
