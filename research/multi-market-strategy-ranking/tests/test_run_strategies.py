import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath('research/multi-market-strategy-ranking/src'))
import run_strategies

def test_make_state():
    df = pd.DataFrame({
        'close': [100, 105, 95, 110, 89],
        'hi55': [100, 100, 100, 100, 100],
        'lo55': [90, 90, 90, 90, 90],
        'hi20x': [100, 100, 100, 100, 100],
        'lo20x': [90, 90, 90, 90, 90],
        'ema200': [99, 99, 99, 99, 100],
        'atr': [2, 2, 2, 2, 2],
        'ema20': [100, 100, 100, 100, 100],
        'st_dir': [1, -1, 1, -1, 1],
        'adx14': [25, 25, 25, 25, 25],
        'ema50': [98, 98, 98, 98, 98],
        'bblow': [90, 90, 90, 90, 90],
        'bbhi': [110, 110, 110, 110, 110],
        'bbmid': [100, 100, 100, 100, 100],
        'rsi14': [40, 60, 40, 60, 40],
        'volsma20x': [100, 100, 100, 100, 100],
        'volume': [200, 200, 200, 200, 200],
        'hi10x': [100, 100, 100, 100, 100],
        'lo10x': [90, 90, 90, 90, 90],
        'macd': [1, -1, 1, -1, 1],
        'macdsig': [0, 0, 0, 0, 0]
    })

    # Just run through them to ensure no crashes and basic shape
    for name in run_strategies.RULES:
        sig = run_strategies.make_state(df, name)
        assert len(sig) == 5
        assert isinstance(sig, np.ndarray)
