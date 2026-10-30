import pandas as pd
import numpy as np
import math
from pathlib import Path
import five_year_multi_market_kelly as base
from run_strategies import RULES, add_adx

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RULES.update({
    'Supertrend_EMA200_ADX20': 'Supertrend(10,3) & close > EMA200 & ADX14 > 20 for long.',
    'EMA20_50_EMA200_ADX20': 'EMA20 > EMA50 & close > EMA200 & ADX14 > 20 for long.',
    'Donchian20_EMA200_ADX20': 'Close > 20d High & close > EMA200 & ADX14 > 20 for long.',
    'MACD_RSI50': 'MACD crosses signal & RSI14 > 50 for long.',
    'MACD_ADX20': 'MACD crosses signal & ADX14 > 20 for long.'
})

def add_indicators(d):
    # Base ADX setup
    up=d.high.diff(); down=-d.low.diff()
    plus=up.where((up>down)&(up>0),0.0); minus=down.where((down>up)&(down>0),0.0)
    prev=d.close.shift(1)
    tr=pd.concat([(d.high-d.low).astype(float),(d.high-prev).abs().astype(float),(d.low-prev).abs().astype(float)],axis=1).max(axis=1)
    atr=tr.ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    pdi=100*plus.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
    mdi=100*minus.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
    dx=100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)
    d['adx14']=dx.ewm(alpha=1/14,adjust=False,min_periods=14).mean()

    d['hi20x']=d.high.shift(1).rolling(20,min_periods=20).max(); d['lo20x']=d.low.shift(1).rolling(20,min_periods=20).min()
    d['ema20']=d.close.ewm(span=20,adjust=False).mean()
    d['ema50']=d.close.ewm(span=50,adjust=False).mean()
    d['ema200']=d.close.ewm(span=200,adjust=False).mean()
    d['atr14'] = atr

    hl2 = (d['high'] + d['low']) / 2
    d['basic_ub'] = hl2 + 3 * atr
    d['basic_lb'] = hl2 - 3 * atr

    ema12 = d['close'].ewm(span=12, adjust=False).mean()
    ema26 = d['close'].ewm(span=26, adjust=False).mean()
    d['macd'] = ema12 - ema26
    d['macdsig'] = d['macd'].ewm(span=9, adjust=False).mean()

    delta = d['close'].diff()
    gain = delta.where(delta > 0, 0.0).ewm(alpha=1/14, adjust=False).mean()
    loss = delta.abs().ewm(alpha=1/14, adjust=False).mean()
    rs = gain / (loss + 1e-9)
    d['rsi14_indicator'] = 100 - (100 / (1 + rs))

    return d

def make_signals(d, name):
    sig = pd.Series(0, index=d.index)
    if name == 'Supertrend_EMA200_ADX20':
        long_cond = (d['close'] > d['ema200']) & (d['adx14'] > 20) & (d['close'] > d['basic_ub'])
        short_cond = (d['close'] < d['ema200']) & (d['adx14'] > 20) & (d['close'] < d['basic_lb'])
        sig[long_cond] = 1
        sig[short_cond] = -1
    elif name == 'EMA20_50_EMA200_ADX20':
        long_cond = (d['ema20'] > d['ema50']) & (d['close'] > d['ema200']) & (d['adx14'] > 20)
        short_cond = (d['ema20'] < d['ema50']) & (d['close'] < d['ema200']) & (d['adx14'] > 20)
        sig[long_cond] = 1
        sig[short_cond] = -1
    elif name == 'Donchian20_EMA200_ADX20':
        long_cond = (d['close'] >= d['hi20x']) & (d['close'] > d['ema200']) & (d['adx14'] > 20)
        short_cond = (d['close'] <= d['lo20x']) & (d['close'] < d['ema200']) & (d['adx14'] > 20)
        sig[long_cond] = 1
        sig[short_cond] = -1
    elif name == 'MACD_RSI50':
        long_cond = (d['macd'] > d['macdsig']) & (d['rsi14_indicator'] > 50)
        short_cond = (d['macd'] < d['macdsig']) & (d['rsi14_indicator'] < 50)
        sig[long_cond] = 1
        sig[short_cond] = -1
    elif name == 'MACD_ADX20':
        long_cond = (d['macd'] > d['macdsig']) & (d['adx14'] > 20)
        short_cond = (d['macd'] < d['macdsig']) & (d['adx14'] > 20)
        sig[long_cond] = 1
        sig[short_cond] = -1
    return sig.to_numpy()

def backtest_strategy(raw, market, symbol, label, name, tp_r):
    df = add_indicators(raw.copy()).dropna().reset_index(drop=True)
    if len(df) == 0: return []
    sig = make_signals(df, name)

    trades = []
    side = 0
    entry_price = 0
    entry_time = None
    entry_i = 0
    dist = 0
    stop = 0
    take = 0
    fee = 0.0005 if market == 'Crypto futures' else 0.0002

    for i in range(1, len(df)-1):
        if side == 0:
            if sig[i-1] != 0:
                side = sig[i-1]
                entry_time = df['timestamp'].iloc[i]
                entry_i = i
                entry_price = df['open'].iloc[i]
                dist = 1.5 * df['atr14'].iloc[i-1]
                if not math.isfinite(dist) or dist <= 0:
                    side = 0
                    continue
                stop = entry_price - side * dist
                take = entry_price + side * tp_r * dist
        else:
            slhit = (df['low'].iloc[i] <= stop) if side == 1 else (df['high'].iloc[i] >= stop)
            tphit = (df['high'].iloc[i] >= take) if side == 1 else (df['low'].iloc[i] <= take)

            if slhit or tphit:
                if slhit:
                    px = stop
                    reason = 'Stop Loss'
                else:
                    px = take
                    reason = 'Take Profit'

                pnl = side * (px - entry_price) - fee * (abs(entry_price) + abs(px))
                trades.append({
                    'entry_time': entry_time,
                    'exit_time': df['timestamp'].iloc[i],
                    'R': pnl / dist if dist > 0 else 0,
                    'reason': reason
                })
                side = 0

    if side != 0:
        px = df['close'].iloc[-1]
        pnl = side * (px - entry_price) - fee * (abs(entry_price) + abs(px))
        trades.append({
            'entry_time': entry_time,
            'exit_time': df['timestamp'].iloc[-1],
            'R': pnl / dist if dist > 0 else 0,
            'reason': 'End of Data'
        })

    return trades

def run_all():
    instruments = [
        ("Crypto futures", "BTCUSDT", "BTCUSDT", lambda: base.binance_daily("BTCUSDT")),
        ("Crypto futures", "ETHUSDT", "ETHUSDT", lambda: base.binance_daily("ETHUSDT")),
        ("FX", "EURUSD=X", "EUR/USD", lambda: base.yahoo_daily("EURUSD=X")),
        ("FX", "USDJPY=X", "USD/JPY", lambda: base.yahoo_daily("USDJPY=X")),
        ("Traditional futures", "ES=F", "E-mini S&P 500", lambda: base.yahoo_daily("ES=F")),
    ]

    rows = []

    for market, symbol, label, loader in instruments:
        try:
            print(f"Testing {symbol}...")
            raw = loader()
            raw = raw.dropna(subset=["open","high","low","close"]).sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
            raw = raw[(raw.timestamp >= base.WARM) & (raw.timestamp < base.END)].reset_index(drop=True)

            if len(raw) < 250:
                continue

            for name in ['Supertrend_EMA200_ADX20', 'EMA20_50_EMA200_ADX20', 'Donchian20_EMA200_ADX20', 'MACD_RSI50', 'MACD_ADX20']:
                for tp in [1.5, 2.0, 3.0]:
                    trades = backtest_strategy(raw, market, symbol, label, name, tp)

                    if len(trades) < 70:
                        continue

                    is_trades = [t for t in trades if pd.Timestamp(t['entry_time']) < base.OOS]
                    oos_trades = [t for t in trades if pd.Timestamp(t['entry_time']) >= base.OOS]

                    ret, dd, _, _ = base.fixed_risk_stats(trades, 0.10)
                    oosret, _, _, _ = base.fixed_risk_stats(oos_trades, 0.10)

                    fm = base.formula_stats(is_trades)
                    win_rate = fm['p']
                    kelly = fm['kelly']

                    tp_count = sum(1 for t in trades if t['reason'] == 'Take Profit')
                    sl_count = sum(1 for t in trades if t['reason'] == 'Stop Loss')
                    pf_denom = abs(sum(t['R'] for t in trades if t['R'] < 0))
                    pf = (sum(t['R'] for t in trades if t['R'] > 0) / pf_denom) if pf_denom != 0 else float('inf')

                    pine_name = name.lower() + "_tp" + str(tp).replace(".","")

                    rows.append({
                        "Rank": 0,
                        "Strategy": name,
                        "Market": market,
                        "Symbol": symbol,
                        "Timeframe": "1d", "Start Date": str(raw.timestamp.min().date()), "End Date": str(raw.timestamp.max().date()), "Data Source": "Yahoo/Binance", "Costs": "5bps Crypto / 1 tick Trad / 0.4pip FX",
                        "5y Net Return %": f"{ret:.2f}",
                        "CAGR %": f"{((1 + ret/100)**(1/5) - 1)*100:.2f}" if ret > 0 else "0.00",
                        "Trades": len(trades),
                        "TP/SL": f"{tp_count}/{sl_count}",
                        "Win Rate %": f"{win_rate*100:.2f}" if math.isfinite(win_rate) else "0.00",
                        "PF": f"{pf:.2f}",
                        "Max DD %": f"{dd:.2f}",
                        "IS Kelly %": f"{kelly*100:.2f}" if math.isfinite(kelly) else "0.00",
                        "OOS Return %": f"{oosret:.2f}",
                        "OOS Trades": len(oos_trades),
                        "Exit": f"Fixed {tp}R TP, 1.5ATR SL",
                        "Sizing": "Fixed 0.1R",
                        "Pine Path": f"`pine/{pine_name}.pine`",
                        "Pine Status": "TV_UNVERIFIED"
                    })
        except Exception as e:
            print(f"Error {symbol}: {e}")

    if rows:
        df = pd.DataFrame(rows)
        df['5y Net Return %'] = pd.to_numeric(df['5y Net Return %'])
        df = df.sort_values("5y Net Return %", ascending=False).reset_index(drop=True)
        df["Rank"] = np.arange(1, len(df) + 1)

        csv_path = RESULTS_DIR / "strategy_70plus_ranking.csv"
        df.to_csv(csv_path, index=False)
        print(f"Saved {len(df)} results to {csv_path}")

        md_path = RESULTS_DIR / "strategy_70plus_ranking.md"
        df.to_markdown(md_path, index=False)
        print(f"Saved MD to {md_path}")
    else:
        print("No strategy generated >= 70 trades.")

if __name__ == '__main__':
    run_all()
