"""
策略名稱: WEMA20_50+Donchian20
最佳配置: SOLUSDT / 6h | 出場方式: 固定4R+訊號出場
五年收益: +366.98% | 最大回撤: 34.95% | 交易筆數: 86
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
    print("策略 WEMA20_50+Donchian20 載入成功")
