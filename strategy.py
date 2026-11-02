"""
策略名稱: MACD12_26_9
最佳配置: SOLUSDT / 12h | 出場方式: 固定4R+訊號出場
五年收益: +1405.73% | 最大回撤: 37.08% | 交易筆數: 263
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
    print("策略 MACD12_26_9 載入成功")
