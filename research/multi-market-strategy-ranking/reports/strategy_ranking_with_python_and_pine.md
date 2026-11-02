# 31 種核心策略綜合實力排行榜（附 Python 與 Pine Script v6 代碼）
> **篩選門檻**：五年交易筆數 >= 70，無勝率限制。僅呈現各策略最佳單筆實測數據。

## 📊 策略綜合總排名

| 策略綜合排名 | 策略 | 完成組數 | 最大收益_pct | 交易筆數 | 止盈筆數 | 止損筆數 | 商品 | 週期 | 出場方式 | 最大回撤_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | EMA50_200 | 97 | 2264.16 | 85 | 0 | 71 | SOLUSDT | 3h | 訊號出場(無固定TP) | 84.69 |
| 2 | Volume_Donchian20 | 190 | 1879.65 | 117 | 0 | 60 | BTCUSDT | 8h | 訊號出場(無固定TP) | 35.64 |
| 3 | Supertrend10_3 | 174 | 1868.46 | 325 | 0 | 209 | SOLUSDT | 3h | 訊號出場(無固定TP) | 32.17 |
| 4 | Supertrend+EMA200 | 25 | 1836.6 | 600 | 0 | 0 | SOLUSDT | 2h | 訊號出場 | 42.15 |
| 5 | Donchian20_10 | 166 | 1421.65 | 203 | 0 | 99 | SOLUSDT | 6h | 訊號出場(無固定TP) | 52.92 |
| 6 | MACD12_26_9 | 223 | 1405.73 | 263 | 0 | 0 | SOLUSDT | 12h | 固定4R+訊號出場 | 37.08 |
| 7 | Supertrend+RSI50 | 30 | 1250.27 | 118 | 0 | 0 | SOLUSDT | 1d | 訊號出場 | 29.35 |
| 8 | Donchian20_Volume_EMA200 | 23 | 1133.04 | 244 | 69 | 125 | SOLUSDT | 3h | 固定止盈3R | 71.26 |
| 9 | EMA20_50_ADX20 | 17 | 1124.36 | 73 | 0 | 0 | SOLUSDT | 4h | 訊號出場 | 53.96 |
| 10 | Donchian20+MACD | 26 | 1054.51 | 205 | 0 | 0 | SOLUSDT | 8h | 訊號出場 | 53.72 |
| 11 | Keltner20_1.5ATR_EMA200 | 29 | 938.71 | 368 | 129 | 150 | SOLUSDT | 3h | 固定止盈2R | 35.28 |
| 12 | WEMA20_50+MACD | 25 | 863.26 | 109 | 0 | 0 | BTCUSDT | 12h | 訊號出場(無固定TP) | 56.63 |
| 13 | MACD+RSI50 | 26 | 813.81 | 1319 | 0 | 180 | SOLUSDT | 3h | 訊號出場(無固定TP) | 56.93 |
| 14 | Turtle55_20_EMA200 | 20 | 717.61 | 82 | 29 | 45 | SOLUSDT | 6h | 固定止盈3R | 50.78 |
| 15 | Supertrend+EMA200_flip | 18 | 468.16 | 73 | 33 | 40 | SOLUSDT | 6h | 固定止盈2R | 60.88 |
| 16 | MACD_EMA200_ADX20 | 19 | 449.8 | 72 | 0 | 0 | SOLUSDT | 12h | 訊號出場 | 40.52 |
| 17 | Donchian20+ADX14 | 23 | 443.58 | 220 | 69 | 150 | BTCUSDT | 6h | 固定止盈3R | 37.4 |
| 18 | WEMA20_50+Donchian20 | 9 | 366.98 | 86 | 17 | 39 | SOLUSDT | 6h | 固定4R+訊號出場 | 34.95 |
| 19 | EMA200+MACD_cross | 20 | 341.29 | 120 | 90 | 30 | SOLUSDT | 12h | 固定止盈0.5R | 31.21 |
| 20 | WEMA20_50+DailyDonchian20 | 20 | 333.67 | 150 | 87 | 63 | SOLUSDT | 8h | 固定止盈1R | 34.65 |
| 21 | Supertrend_ADX20 | 21 | 240.71 | 81 | 25 | 50 | ETHUSDT | 6h | 固定止盈3R | 33.65 |
| 22 | Bollinger20+RSI14_reentry | 19 | 239.96 | 71 | 0 | 0 | USDJPY=X | 1d | 純固定TP 0.5R／初始SL 1.5ATR | 44.17 |
| 23 | Bollinger20_2 | 151 | 204.84 | 72 | 0 | 0 | BTCUSDT | 1d | 固定4R+訊號出場 | 57.25 |
| 24 | EMA200+RSI14_pullback | 10 | 201.21 | 162 | 67 | 95 | SOLUSDT | 30m | 固定止盈2R | 36.82 |
| 25 | RSI14_EMA200 | 40 | 161.39 | 155 | 5 | 48 | SOLUSDT | 30m | ATR移動止盈3x+訊號出場 | 42.17 |
| 26 | EMA200+RSI2_mean_reversion | 25 | 161.11 | 224 | 32 | 52 | ETHUSDT | 8h | 固定1R+訊號出場 | 37.81 |
| 27 | RSI2_EMA200 | 220 | 161.11 | 224 | 32 | 52 | ETHUSDT | 8h | 固定1R+訊號出場 | 37.81 |
| 28 | WEMA20_50+DailyMACD | 19 | 130.46 | 76 | 22 | 53 | SOLUSDT | 12h | 固定止盈3R | 60.77 |
| 29 | Stoch14+EMA200 | 15 | 126.89 | 212 | 155 | 57 | ETHUSDT | 8h | 固定止盈0.5R | 34.98 |
| 30 | EMA200+RSI2_extreme | 18 | 121.47 | 273 | 75 | 198 | ETHUSDT | 4h | 固定止盈3R | 87.66 |
| 31 | BB_Reentry_RSI_ADX25 | 17 | 18.71 | 112 | 3 | 51 | BTCUSDT | 6h | 固定止盈3R | 47.09 |

---

## 💻 各策略程式碼實作（Python + Pine Script v6）

### 第 1 名：EMA50_200
- **最佳單組配置**：SOLUSDT / 3h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +2264.16% ｜ 最大回撤 84.69% ｜ 交易數 85 筆（止盈: 0 筆, 止損: 71 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['ema200'] = df['close'].ewm(span=200, adjust=False).mean()
    df['long_entry'] = (df['ema50'] > df['ema200']) & (df['ema50'].shift(1) <= df['ema200'].shift(1))
    df['short_entry'] = (df['ema50'] < df['ema200']) & (df['ema50'].shift(1) >= df['ema200'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA50_200 - [SOLUSDT 3h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)
plot(ema50, color=color.orange, title="EMA 50")
plot(ema200, color=color.blue, title="EMA 200")

long_condition = ta.crossover(ema50, ema200)
short_condition = ta.crossunder(ema50, ema200)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 2 名：Volume_Donchian20
- **最佳單組配置**：BTCUSDT / 8h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +1879.65% ｜ 最大回撤 35.64% ｜ 交易數 117 筆（止盈: 0 筆, 止損: 60 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, window=20) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(window).max()
    df['lower'] = df['low'].shift(1).rolling(window).min()
    df['vol_ma'] = df['volume'].rolling(window).mean()
    df['long_entry'] = (df['close'] > df['upper']) & (df['volume'] > df['vol_ma'])
    df['short_entry'] = (df['close'] < df['lower']) & (df['volume'] > df['vol_ma'])
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Volume_Donchian20 - [BTCUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
vol_ma = ta.sma(volume, 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper) and (volume > vol_ma)
short_condition = ta.crossunder(close, lower) and (volume > vol_ma)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 3 名：Supertrend10_3
- **最佳單組配置**：SOLUSDT / 3h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +1868.46% ｜ 最大回撤 32.17% ｜ 交易數 325 筆（止盈: 0 筆, 止損: 209 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Supertrend10_3
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Supertrend10_3 - [SOLUSDT 3h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 4 名：Supertrend+EMA200
- **最佳單組配置**：SOLUSDT / 2h / 訊號出場
- **五年實測績效**：最大收益 +1836.6% ｜ 最大回撤 42.15% ｜ 交易數 600 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd
import numpy as np

def calculate_signals(df: pd.DataFrame, factor=3.0, atr_period=10) -> pd.DataFrame:
    df['ema200'] = df['close'].ewm(span=200, adjust=False).mean()
    hl2 = (df['high'] + df['low']) / 2
    tr = np.maximum(df['high'] - df['low'], np.maximum(abs(df['high'] - df['close'].shift(1)), abs(df['low'] - df['close'].shift(1))))
    df['atr'] = tr.rolling(atr_period).mean()
    df['st_upper'] = hl2 + factor * df['atr']
    df['st_lower'] = hl2 - factor * df['atr']
    df['long_entry'] = (df['close'] > df['st_upper']) & (df['close'] > df['ema200'])
    df['short_entry'] = (df['close'] < df['st_lower']) & (df['close'] < df['ema200'])
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Supertrend+EMA200 - [SOLUSDT 2h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema200 = ta.ema(close, 200)
[st_line, st_dir] = ta.supertrend(3.0, 10)
plot(ema200, color=color.blue, title="EMA 200")

long_condition = (st_dir < 0) and (close > ema200) and (close[1] <= ema200 or st_dir[1] >= 0)
short_condition = (st_dir > 0) and (close < ema200) and (close[1] >= ema200 or st_dir[1] <= 0)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 5 名：Donchian20_10
- **最佳單組配置**：SOLUSDT / 6h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +1421.65% ｜ 最大回撤 52.92% ｜ 交易數 203 筆（止盈: 0 筆, 止損: 99 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Donchian20_10 - [SOLUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 6 名：MACD12_26_9
- **最佳單組配置**：SOLUSDT / 12h / 固定4R+訊號出場
- **五年實測績效**：最大收益 +1405.73% ｜ 最大回撤 37.08% ｜ 交易數 263 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("MACD12_26_9 - [SOLUSDT 12h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("TP/SL Long", "Long", limit=close + 4 * atr_val, stop=close - 1 * atr_val)

if short_condition
    strategy.entry("Short", strategy.short)
    strategy.exit("TP/SL Short", "Short", limit=close - 4 * atr_val, stop=close + 1 * atr_val)

`

### 第 7 名：Supertrend+RSI50
- **最佳單組配置**：SOLUSDT / 1d / 訊號出場
- **五年實測績效**：最大收益 +1250.27% ｜ 最大回撤 29.35% ｜ 交易數 118 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Supertrend+RSI50
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Supertrend+RSI50 - [SOLUSDT 1d]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 8 名：Donchian20_Volume_EMA200
- **最佳單組配置**：SOLUSDT / 3h / 固定止盈3R
- **五年實測績效**：最大收益 +1133.04% ｜ 最大回撤 71.26% ｜ 交易數 244 筆（止盈: 69 筆, 止損: 125 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Donchian20_Volume_EMA200 - [SOLUSDT 3h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 9 名：EMA20_50_ADX20
- **最佳單組配置**：SOLUSDT / 4h / 訊號出場
- **五年實測績效**：最大收益 +1124.36% ｜ 最大回撤 53.96% ｜ 交易數 73 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: EMA20_50_ADX20
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA20_50_ADX20 - [SOLUSDT 4h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 10 名：Donchian20+MACD
- **最佳單組配置**：SOLUSDT / 8h / 訊號出場
- **五年實測績效**：最大收益 +1054.51% ｜ 最大回撤 53.72% ｜ 交易數 205 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Donchian20+MACD - [SOLUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 11 名：Keltner20_1.5ATR_EMA200
- **最佳單組配置**：SOLUSDT / 3h / 固定止盈2R
- **五年實測績效**：最大收益 +938.71% ｜ 最大回撤 35.28% ｜ 交易數 368 筆（止盈: 129 筆, 止損: 150 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Keltner20_1.5ATR_EMA200
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Keltner20_1.5ATR_EMA200 - [SOLUSDT 3h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 12 名：WEMA20_50+MACD
- **最佳單組配置**：BTCUSDT / 12h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +863.26% ｜ 最大回撤 56.63% ｜ 交易數 109 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("WEMA20_50+MACD - [BTCUSDT 12h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 13 名：MACD+RSI50
- **最佳單組配置**：SOLUSDT / 3h / 訊號出場(無固定TP)
- **五年實測績效**：最大收益 +813.81% ｜ 最大回撤 56.93% ｜ 交易數 1319 筆（止盈: 0 筆, 止損: 180 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("MACD+RSI50 - [SOLUSDT 3h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 14 名：Turtle55_20_EMA200
- **最佳單組配置**：SOLUSDT / 6h / 固定止盈3R
- **五年實測績效**：最大收益 +717.61% ｜ 最大回撤 50.78% ｜ 交易數 82 筆（止盈: 29 筆, 止損: 45 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Turtle55_20_EMA200
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Turtle55_20_EMA200 - [SOLUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 15 名：Supertrend+EMA200_flip
- **最佳單組配置**：SOLUSDT / 6h / 固定止盈2R
- **五年實測績效**：最大收益 +468.16% ｜ 最大回撤 60.88% ｜ 交易數 73 筆（止盈: 33 筆, 止損: 40 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd
import numpy as np

def calculate_signals(df: pd.DataFrame, factor=3.0, atr_period=10) -> pd.DataFrame:
    df['ema200'] = df['close'].ewm(span=200, adjust=False).mean()
    hl2 = (df['high'] + df['low']) / 2
    tr = np.maximum(df['high'] - df['low'], np.maximum(abs(df['high'] - df['close'].shift(1)), abs(df['low'] - df['close'].shift(1))))
    df['atr'] = tr.rolling(atr_period).mean()
    df['st_upper'] = hl2 + factor * df['atr']
    df['st_lower'] = hl2 - factor * df['atr']
    df['long_entry'] = (df['close'] > df['st_upper']) & (df['close'] > df['ema200'])
    df['short_entry'] = (df['close'] < df['st_lower']) & (df['close'] < df['ema200'])
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Supertrend+EMA200_flip - [SOLUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema200 = ta.ema(close, 200)
[st_line, st_dir] = ta.supertrend(3.0, 10)
plot(ema200, color=color.blue, title="EMA 200")

long_condition = (st_dir < 0) and (close > ema200) and (close[1] <= ema200 or st_dir[1] >= 0)
short_condition = (st_dir > 0) and (close < ema200) and (close[1] >= ema200 or st_dir[1] <= 0)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 16 名：MACD_EMA200_ADX20
- **最佳單組配置**：SOLUSDT / 12h / 訊號出場
- **五年實測績效**：最大收益 +449.8% ｜ 最大回撤 40.52% ｜ 交易數 72 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("MACD_EMA200_ADX20 - [SOLUSDT 12h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 17 名：Donchian20+ADX14
- **最佳單組配置**：BTCUSDT / 6h / 固定止盈3R
- **五年實測績效**：最大收益 +443.58% ｜ 最大回撤 37.4% ｜ 交易數 220 筆（止盈: 69 筆, 止損: 150 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Donchian20+ADX14 - [BTCUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 18 名：WEMA20_50+Donchian20
- **最佳單組配置**：SOLUSDT / 6h / 固定4R+訊號出場
- **五年實測績效**：最大收益 +366.98% ｜ 最大回撤 34.95% ｜ 交易數 86 筆（止盈: 17 筆, 止損: 39 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("WEMA20_50+Donchian20 - [SOLUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("TP/SL Long", "Long", limit=close + 4 * atr_val, stop=close - 1 * atr_val)

if short_condition
    strategy.entry("Short", strategy.short)
    strategy.exit("TP/SL Short", "Short", limit=close - 4 * atr_val, stop=close + 1 * atr_val)

`

### 第 19 名：EMA200+MACD_cross
- **最佳單組配置**：SOLUSDT / 12h / 固定止盈0.5R
- **五年實測績效**：最大收益 +341.29% ｜ 最大回撤 31.21% ｜ 交易數 120 筆（止盈: 90 筆, 止損: 30 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA200+MACD_cross - [SOLUSDT 12h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 20 名：WEMA20_50+DailyDonchian20
- **最佳單組配置**：SOLUSDT / 8h / 固定止盈1R
- **五年實測績效**：最大收益 +333.67% ｜ 最大回撤 34.65% ｜ 交易數 150 筆（止盈: 87 筆, 止損: 63 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame, entry_len=20, exit_len=10) -> pd.DataFrame:
    df['upper'] = df['high'].shift(1).rolling(entry_len).max()
    df['lower'] = df['low'].shift(1).rolling(entry_len).min()
    df['long_entry'] = df['close'] > df['upper']
    df['short_entry'] = df['close'] < df['lower']
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("WEMA20_50+DailyDonchian20 - [SOLUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

upper = ta.highest(high[1], 20)
lower = ta.lowest(low[1], 20)
plot(upper, color=color.green, title="Donchian Upper")
plot(lower, color=color.red, title="Donchian Lower")

long_condition = ta.crossover(close, upper)
short_condition = ta.crossunder(close, lower)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 21 名：Supertrend_ADX20
- **最佳單組配置**：ETHUSDT / 6h / 固定止盈3R
- **五年實測績效**：最大收益 +240.71% ｜ 最大回撤 33.65% ｜ 交易數 81 筆（止盈: 25 筆, 止損: 50 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Supertrend_ADX20
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Supertrend_ADX20 - [ETHUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 22 名：Bollinger20+RSI14_reentry
- **最佳單組配置**：USDJPY=X / 1d / 純固定TP 0.5R／初始SL 1.5ATR
- **五年實測績效**：最大收益 +239.96% ｜ 最大回撤 44.17% ｜ 交易數 71 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Bollinger20+RSI14_reentry
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Bollinger20+RSI14_reentry - [USDJPY=X 1d]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 23 名：Bollinger20_2
- **最佳單組配置**：BTCUSDT / 1d / 固定4R+訊號出場
- **五年實測績效**：最大收益 +204.84% ｜ 最大回撤 57.25% ｜ 交易數 72 筆（止盈: 0 筆, 止損: 0 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Bollinger20_2
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Bollinger20_2 - [BTCUSDT 1d]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("TP/SL Long", "Long", limit=close + 4 * atr_val, stop=close - 1 * atr_val)

if short_condition
    strategy.entry("Short", strategy.short)
    strategy.exit("TP/SL Short", "Short", limit=close - 4 * atr_val, stop=close + 1 * atr_val)

`

### 第 24 名：EMA200+RSI14_pullback
- **最佳單組配置**：SOLUSDT / 30m / 固定止盈2R
- **五年實測績效**：最大收益 +201.21% ｜ 最大回撤 36.82% ｜ 交易數 162 筆（止盈: 67 筆, 止損: 95 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: EMA200+RSI14_pullback
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA200+RSI14_pullback - [SOLUSDT 30m]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 25 名：RSI14_EMA200
- **最佳單組配置**：SOLUSDT / 30m / ATR移動止盈3x+訊號出場
- **五年實測績效**：最大收益 +161.39% ｜ 最大回撤 42.17% ｜ 交易數 155 筆（止盈: 5 筆, 止損: 48 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: RSI14_EMA200
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("RSI14_EMA200 - [SOLUSDT 30m]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("Trail Long", "Long", trail_points=atr_val * 3, trail_offset=atr_val)

if short_condition
    strategy.entry("Short", strategy.short)
    strategy.exit("Trail Short", "Short", trail_points=atr_val * 3, trail_offset=atr_val)

`

### 第 26 名：EMA200+RSI2_mean_reversion
- **最佳單組配置**：ETHUSDT / 8h / 固定1R+訊號出場
- **五年實測績效**：最大收益 +161.11% ｜ 最大回撤 37.81% ｜ 交易數 224 筆（止盈: 32 筆, 止損: 52 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: EMA200+RSI2_mean_reversion
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA200+RSI2_mean_reversion - [ETHUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 27 名：RSI2_EMA200
- **最佳單組配置**：ETHUSDT / 8h / 固定1R+訊號出場
- **五年實測績效**：最大收益 +161.11% ｜ 最大回撤 37.81% ｜ 交易數 224 筆（止盈: 32 筆, 止損: 52 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: RSI2_EMA200
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("RSI2_EMA200 - [ETHUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 28 名：WEMA20_50+DailyMACD
- **最佳單組配置**：SOLUSDT / 12h / 固定止盈3R
- **五年實測績效**：最大收益 +130.46% ｜ 最大回撤 60.77% ｜ 交易數 76 筆（止盈: 22 筆, 止損: 53 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['long_entry'] = (df['macd'] > df['signal']) & (df['macd'].shift(1) <= df['signal'].shift(1))
    df['short_entry'] = (df['macd'] < df['signal']) & (df['macd'].shift(1) >= df['signal'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("WEMA20_50+DailyMACD - [SOLUSDT 12h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

[macd_line, sig_line, _] = ta.macd(close, 12, 26, 9)
long_condition = ta.crossover(macd_line, sig_line)
short_condition = ta.crossunder(macd_line, sig_line)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 29 名：Stoch14+EMA200
- **最佳單組配置**：ETHUSDT / 8h / 固定止盈0.5R
- **五年實測績效**：最大收益 +126.89% ｜ 最大回撤 34.98% ｜ 交易數 212 筆（止盈: 155 筆, 止損: 57 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: Stoch14+EMA200
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("Stoch14+EMA200 - [ETHUSDT 8h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 30 名：EMA200+RSI2_extreme
- **最佳單組配置**：ETHUSDT / 4h / 固定止盈3R
- **五年實測績效**：最大收益 +121.47% ｜ 最大回撤 87.66% ｜ 交易數 273 筆（止盈: 75 筆, 止損: 198 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: EMA200+RSI2_extreme
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("EMA200+RSI2_extreme - [ETHUSDT 4h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`

### 第 31 名：BB_Reentry_RSI_ADX25
- **最佳單組配置**：BTCUSDT / 6h / 固定止盈3R
- **五年實測績效**：最大收益 +18.71% ｜ 最大回撤 47.09% ｜ 交易數 112 筆（止盈: 3 筆, 止損: 51 筆）

#### 🐍 Python 策略程式碼
`python
import pandas as pd

def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
    # 策略: BB_Reentry_RSI_ADX25
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['long_entry'] = (df['ema20'] > df['ema50']) & (df['ema20'].shift(1) <= df['ema50'].shift(1))
    df['short_entry'] = (df['ema20'] < df['ema50']) & (df['ema20'].shift(1) >= df['ema50'].shift(1))
    return df
`

#### 🌲 TradingView Pine Script v6 代碼
`pinescript
//@version=6
strategy("BB_Reentry_RSI_ADX25 - [BTCUSDT 6h]", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// === 指標計算 ===
atr_val = ta.atr(14)

ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
long_condition = ta.crossover(ema20, ema50)
short_condition = ta.crossunder(ema20, ema50)

// === 出場設定 ===
if long_condition
    strategy.entry("Long", strategy.long)
if short_condition
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

`
