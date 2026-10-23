# Pine Script v6 策略索引與說明文件

本資料夾包含由五年的多市場策略 Python 原始碼轉譯而成的獨立、可檢查 Pine Script v6 策略腳本 (`.pine`)，以及與 Python 實作對照之索引說明。

## 策略總數與去重核驗說明

在 4 個 Python 策略腳本中，共定義了 32 個策略條目。產出的排名結果數據表 (`complete_ranking_9556.csv.gz` 與 `strategy_max_return_kelly_details.csv`) 中包含 31 個不重複策略名稱：
1. **策略去重（30 種獨立邏輯）**：經逐項核驗 Python 原始碼，`RSI2_EMA200`（位於 `five_year_multi_market_kelly.py`）與 `EMA200+RSI2_mean_reversion`（位於 `five_year_compound_strategy_sweep.py`）之進出場邏輯完全相同。因此將兩者合併歸納為 1 個獨立 Pine 腳本 (`rsi2_ema200.pine`)，共建立 **30 份獨立 Pine Script v6 策略**。
2. **重複定義條目說明**：`EMA200+RSI14_pullback` 同時出現在 `five_year_compound_strategy_sweep.py` 與 `five_year_low_drawdown_fixed_rr.py` 中，名稱與邏輯相同，因此在總榜中維持 31 個策略名稱。
3. **參數與配置獨立化**：每個 Pine 檔案對應一種策略邏輯；商品與週期由使用者在 TradingView 圖表選擇，風險/出場參數以腳本 input 提供時可調。策略訊號參數依 Python 原始定義，不以配置差異複製腳本。

---

## 策略索引對照表 (Index Table)

| 策略名稱 (Ranking Name) | 去重邏輯分類 | Python 檔 / 函式 | Pine Script 檔案 | 代表排名配置 (商品 | 市場 | 週期 | 倉位 | 風控/出場) | Cost & Engine 注意事項 | TV 實測狀態 |
|---|---|---|---|---|---|---|
| **MACD12_26_9** | MACD (12,26,9) 雙線交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/macd12_26_9.pine`](macd12_26_9.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Supertrend+RSI50** | Supertrend(10,3) + RSI14>50 複合策略 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_rsi50.pine`](supertrend_rsi50.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.1%)<br>風控: 訊號出場(無固定TP) | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Supertrend10_3** | Supertrend(10,3) 趨勢追蹤 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/supertrend10_3.pine`](supertrend10_3.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.5%)<br>風控: 訊號出場(無固定TP) | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Supertrend+EMA200** | Supertrend(10,3) + EMA200 濾網 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/supertrend_ema200.pine`](supertrend_ema200.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (23.5%)<br>風控: 訊號出場(無固定TP) | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Stoch14+EMA200** | Stoch(14) 超賣/超買 + EMA200 均值回歸 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/stoch14_ema200.pine`](stoch14_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.9%)<br>風控: 純固定TP 2.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **Supertrend+EMA200_flip** | Supertrend(10,3) 翻轉 + EMA200 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/supertrend_ema200_flip.pine`](supertrend_ema200_flip.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (44.4%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **WEMA20_50+Donchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 突破 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_donchian20.pine`](wema20_50_donchian20.pine) | **NQ=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (46.0%)<br>風控: 固定4R+訊號出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗；週線 request.security[1] (lookahead_on) | **未測** |
| **WEMA20_50+MACD** | 週線 EMA(20/50) + 日線 MACD 交叉 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/wema20_50_macd.pine`](wema20_50_macd.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (26.5%)<br>風控: ATR移動止盈2x+訊號出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗；週線 request.security[1] (lookahead_on) | **未測** |
| **EMA20_50_ADX20** | EMA(20/50) 交叉 + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/ema20_50_adx20.pine`](ema20_50_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (77.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Donchian20_10** | Donchian(20) 進場 / Donchian(10) 出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/donchian20_10.pine`](donchian20_10.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (39.8%)<br>風控: 固定1R+訊號出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **EMA50_200** | EMA(50/200) 黃金/死亡交叉 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/ema50_200.pine`](ema50_200.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 固定1R (初始本金風險10%; IS全凱利=0%)<br>風控: 反向均線交叉出場 | Crypto cost: Pine commission 0.1%/side approximates Python fee+slippage; not identical | **未測** |
| **WEMA20_50+DailyDonchian20** | 週線 EMA(20/50) + 日線 Donchian(20) 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_donchian20.pine`](wema20_50_daily_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (24.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗；週線 request.security[1] (lookahead_on) | **未測** |
| **MACD+RSI50** | MACD 交叉 + RSI(14)>50 趨勢動能 | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/macd_rsi50.pine`](macd_rsi50.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (10.5%)<br>風控: 訊號出場(無固定TP) | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Donchian20_Volume_EMA200** | Donchian(20) + 1.5倍量能 + EMA200 濾網 | `run_strategies.py`<br>`make_state()` | [`pine/donchian20_volume_ema200.pine`](donchian20_volume_ema200.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (63.5%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **Keltner20_1.5ATR_EMA200** | Keltner(20, 1.5ATR) 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/keltner20_15atr_ema200.pine`](keltner20_15atr_ema200.pine) | **YM=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (47.2%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **Donchian20+ADX14** | Donchian20+ADX14 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/donchian20_adx14.pine`](donchian20_adx14.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (IS Kelly: 20.281839%)<br>風控: 純固定TP 1.5R／初始SL 1.5ATR | Crypto cost: Pine commission 0.1%/side approximates Python fee+slippage; not identical | **未測** |
| **EMA200+MACD_cross** | EMA200 方向 + MACD 交叉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_macd_cross.pine`](ema200_macd_cross.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (20.6%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **Donchian20+MACD** | Donchian20+MACD | `five_year_compound_strategy_sweep.py`<br>`custom_signals()` | [`pine/donchian20_macd.pine`](donchian20_macd.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (IS Kelly: 21.555166%)<br>風控: 訊號出場(無固定TP) | Crypto cost: Pine commission 0.1%/side approximates Python fee+slippage; not identical | **未測** |
| **Turtle55_20_EMA200** | Turtle 55/20 通道突破 + EMA200 | `run_strategies.py`<br>`make_state()` | [`pine/turtle55_20_ema200.pine`](turtle55_20_ema200.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (34.3%)<br>風控: IS選定固定TP 1.5R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Bollinger20+RSI14_reentry** | 布林(20,2σ) 帶外返回 + RSI14 濾網 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/bollinger20_rsi14_reentry.pine`](bollinger20_rsi14_reentry.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (17.8%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Supertrend_ADX20** | Supertrend(10,3) + ADX(14)>20 強趨勢 | `run_strategies.py`<br>`make_state()` | [`pine/supertrend_adx20.pine`](supertrend_adx20.pine) | **DOGEUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (40.6%)<br>風控: IS選定固定TP 0.75R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **Volume_Donchian20** | 量能 1.5倍 + Donchian(20) 突破 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/volume_donchian20.pine`](volume_donchian20.pine) | **GC=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (27.7%)<br>風控: 固定4R+訊號出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **RSI2_EMA200<br>*(等價: EMA200+RSI2_mean_reversion)*** | EMA200 趨勢 + RSI(2) 極端回歸 (去重邏輯) | `five_year_multi_market_kelly.py / five_year_compound_strategy_sweep.py`<br>`make_signals() / custom_signals()` | [`pine/rsi2_ema200.pine`](rsi2_ema200.pine) | **ES=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (30.9%)<br>風控: 固定1R+訊號出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **EMA200+RSI2_extreme** | EMA200 趨勢 + RSI(2)<5/95 極致反轉 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/ema200_rsi2_extreme.pine`](ema200_rsi2_extreme.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (13.5%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **EMA200+RSI14_pullback** | EMA200 趨勢 + RSI(14) 30/70 回檔拉回 | `five_year_compound_strategy_sweep.py / five_year_low_drawdown_fixed_rr.py`<br>`custom_signals() / signals()` | [`pine/ema200_rsi14_pullback.pine`](ema200_rsi14_pullback.pine) | **ETHUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (55.3%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **WEMA20_50+DailyMACD** | 週線 EMA(20/50) + 日線 MACD 固定盈虧 | `five_year_low_drawdown_fixed_rr.py`<br>`signals()` | [`pine/wema20_50_daily_macd.pine`](wema20_50_daily_macd.pine) | **SOLUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.7%)<br>風控: 純固定TP 3.0R／初始SL 1.5ATR | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗；週線 request.security[1] (lookahead_on) | **未測** |
| **Bollinger20_2** | 布林通道(20,2σ) 帶外返回中軌出場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/bollinger20_2.pine`](bollinger20_2.pine) | **SI=F** (Traditional futures)<br>週期: 1D (日線)<br>部位: 全凱利 (19.1%)<br>風控: ATR移動止盈2x+訊號出場 | 已依Python信號類型修正轉換/事件門控；期貨成本與合約pointvalue仍待TV核驗 | **未測** |
| **MACD_EMA200_ADX20** | MACD 交叉 + EMA200 趨勢 + ADX>20 | `run_strategies.py`<br>`make_state()` | [`pine/macd_ema200_adx20.pine`](macd_ema200_adx20.pine) | **BTCUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (15.1%)<br>風控: IS選定固定TP 3R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |
| **BB_Reentry_RSI_ADX25** | 布林返回 + RSI + ADX<25 低動能震盪 | `run_strategies.py`<br>`make_state()` | [`pine/bb_reentry_rsi_adx25.pine`](bb_reentry_rsi_adx25.pine) | **AUDUSD=X** (FX)<br>週期: 1D (日線)<br>部位: 半凱利 (31.4%)<br>風控: IS選定固定TP 1R／初始SL 1.5ATR＋策略出場 | 已依Python信號類型修正轉換/事件門控；FX成本與pointvalue仍待TV核驗 | **未測** |
| **RSI14_EMA200** | EMA200 趨勢 + RSI(14) 超賣/超買進場 | `five_year_multi_market_kelly.py`<br>`make_signals()` | [`pine/rsi14_ema200.pine`](rsi14_ema200.pine) | **XRPUSDT** (Crypto futures)<br>週期: 1D (日線)<br>部位: 全凱利 (23.8%)<br>風控: 固定2R+訊號出場 | 已依Python信號類型修正轉換/事件門控；成本與商品pointvalue仍待TV核驗 | **未測** |

---

## Python 實作與 TradingView / Pine Script 平台差異與限制說明

已在此 PR 分支修正可直接對照 Python 的狀態轉換、離散事件門控與交叉/突破事件條件；例如布林回歸、Donchian 出場、EMA/MACD 交叉及 Supertrend 方向翻轉。這些修改只重現來源規則，沒有改變 Python 的交易規則或倉位比例。

**仍不可宣稱已完全等價或通過測試：**
- Pine v6 編譯器與 TradingView 回測尚未執行；30 份狀態一律為「未測」。
- TradingView 的委託撮合與 Python bar-loop 在入場同根 K 棒的 SL/TP、同根碰到多個價位及反轉成交上可能不同。
- 加密成本目前以 0.1%/邊 commission 近似 Python 5bps 手續費 + 5bps 價格滑價；commission 不是滑價，不能視為完全相同。FX/期貨成本與 pointvalue 也需用指定 TradingView 商品逐一核驗。
- 週線 EMA 的 TradingView 週界/時區須與 Python UTC W-SUN 週線分桶比對。
- `EMA200+RSI14_pullback` 在 compound Python 與 fixed-RR Python 中同名但退出方式不同；目前單一 Pine 檔只對應 fixed-RR 事件版本，compound 的持續狀態/訊號出場版本仍需補成明確 exit-mode，避免同名規則漏測。

**執行狀態：** 所有 30 份策略維持「未測」；沒有 TradingView 真正回測輸出的項目，不填績效估算。
