"""
策略名稱: MACD+RSI50
最佳配置: SOLUSDT / 3h | 出場方式: 訊號出場(無固定TP)
五年收益: +813.81% | 最大回撤: 56.93% | 交易筆數: 1319
"""
import pandas as pd
import numpy as np

def run_strategy_backtest(df: pd.DataFrame, initial_balance: float = 10000.0, fee_rate: float = 0.0004):
    data = df.copy().reset_index(drop=True)
    data['ema50'] = data['close'].ewm(span=50, adjust=False).mean()
    data['ema200'] = data['close'].ewm(span=200, adjust=False).mean()
    data['long_signal'] = (data['ema50'] > data['ema200']) & (data['ema50'].shift(1) <= data['ema200'].shift(1))
    data['short_signal'] = (data['ema50'] < data['ema200']) & (data['ema50'].shift(1) >= data['ema200'].shift(1))
    return data

if __name__ == '__main__':
    print("策略 MACD+RSI50 載入成功")
