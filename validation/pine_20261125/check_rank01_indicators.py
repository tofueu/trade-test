"""Compare draft-recursion math with original pandas functions; no performance claim."""
import ast
import numpy as np
import pandas as pd
from pathlib import Path

source = Path(r'C:\Users\User\trade-test\research\multi-market-strategy-ranking\src\five_year_multi_market_kelly.py')
module = ast.parse(source.read_text(encoding='utf-8-sig'))
nodes = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in ('rsi', 'indicators', 'make_signals')]
scope = {'np': np, 'pd': pd, 'STRATS': [('Donchian20_10_TP3R', 3), ('MACD12_26_9_TP2R', 2), ('RSI14_EMA200_TP2R', 2), ('EMA50_200_TP3R', 3)]}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), scope)

# Deterministic fixtures exercise crossings, initial ATR and flat bars only.
# Fixture values are never written as historical market data or ranking results.
for close in [100 + np.sin(np.arange(1200) / 27) * 15, np.full(1200, 100.)]:
    raw = pd.DataFrame({'timestamp': pd.date_range('2026-10-11', periods=len(close), freq='3h', tz='UTC'), 'open': close, 'high': close + .3, 'low': close - .3, 'close': close, 'volume': 100.})
    reference = scope['indicators'](raw)
    def recursive(values, alpha):
        output = [float(values[0])]
        for value in values[1:]:
            output.append(output[-1] if output[-1] == float(value) else (1-alpha) * output[-1] + alpha * float(value))
        return np.array(output)
    e50 = recursive(close, 2/51)
    e200 = recursive(close, 2/201)
    previous = np.r_[np.nan, close[:-1]]
    tr = np.nanmax(np.array([raw.high - raw.low, abs(raw.high-previous), abs(raw.low-previous)]), axis=0)
    atr = recursive(tr, 1/14)
    np.testing.assert_allclose(e50, reference.ema50, atol=1e-12)
    np.testing.assert_allclose(e200, reference.ema200, atol=1e-12)
    np.testing.assert_allclose(atr[13:], reference.atr.iloc[13:], atol=1e-12)
    state = 0
    states = []
    for i in range(len(close)):
        if i and e50[i] > e200[i] and e50[i-1] <= e200[i-1]: state = 1
        elif i and e50[i] < e200[i] and e50[i-1] >= e200[i-1]: state = -1
        states.append(state)
    np.testing.assert_array_equal(states, scope['make_signals'](reference, 'EMA50_200_TP3R'))

draft = (Path(__file__).parent / 'drafts/rank_01.pine').read_text(encoding='utf-8')
assert '13.67442526787219' in draft
assert 'endTime' not in draft and 'limitTestEnd' not in draft
assert 'calc_on_order_fills=false' in draft
assert 'from_entry="Long", loss=stopTicks' in draft
print('PASS: draft EMA/ATR recursion and crossover state math vs original Python')
print('NOT RUN: Pine compiler, real TradingView fills, historical performance parity')
