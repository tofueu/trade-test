import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath('research/multi-market-strategy-ranking/src'))
import five_year_multi_market_kelly as base
from run_strategies import add_adx

def test_indicators():
    df = pd.DataFrame({
        'open': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        'high': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        'low': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'close': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
        'volume': [100]*16,
        'timestamp': pd.date_range('2021-01-01', periods=16)
    })
    res = base.indicators(df)
    assert 'atr' in res.columns
    assert 'ema50' in res.columns
    assert 'macd' in res.columns
    assert len(res) == 16

def test_add_adx():
    df = pd.DataFrame({
        'open': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        'high': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        'low': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'close': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
        'volume': [100]*16,
        'timestamp': pd.date_range('2021-01-01', periods=16)
    })
    res = add_adx(df)
    assert 'adx14' in res.columns
    assert len(res) == 16
