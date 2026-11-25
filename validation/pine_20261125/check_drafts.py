"""Source/transition checks only. This is not a Pine compiler or a market backtest."""
from pathlib import Path
import ast
from types import SimpleNamespace
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parent
for rank in (3, 6, 7):
    code = (root / 'drafts' / f'rank_{rank:02}.pine').read_text(encoding='utf-8')
    assert 'endTime' not in code and 'limitTestEnd' not in code
    assert 'End of test window' not in code
    if rank in (3, 7):
        assert 'previousSignalState != 1' in code
        assert 'previousSignalState != -1' in code
    if rank == 3:
        assert 'stopDistance = atrMult * atr14\n' in code
        assert 'signalState != 1' in code
        assert 'signalState != -1' in code
        assert 'nz(signalState[1], 0) !=' not in code

# Use the original Python execution function on a deterministic fixture solely
# to verify reversal/next-open timing after the old end date. These are not prices
# or performance results and are never added to strategy rankings.
source = Path(r'C:\Users\User\trade-test\research\multi-market-strategy-ranking\src\five_year_exit_method_sweep.py')
tree = ast.parse(source.read_text(encoding='utf-8-sig'))
function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'backtest')
base = SimpleNamespace(START=pd.Timestamp('2021-10-10', tz='UTC'),
    indicators=lambda data: data, make_signals=lambda data, name: data['fixture_signal'].to_numpy(),
    costs=lambda market, symbol: (0.0, 0.0))
scope = {'base': base, 'pd': pd, 'np': np}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), scope)
fixture = pd.DataFrame({'timestamp': pd.date_range('2026-11-20', periods=6, freq='h', tz='UTC'),
    'open': 100., 'high': 100.1, 'low': 99.9, 'close': 100., 'atr': 1.,
    'fixture_signal': [0, 1, -1, -1, 0, 0]})
trades = scope['backtest'](fixture, 'fixture', 'fixture', 'fixture', None, None)
assert len(trades) == 2
assert [t['side'] for t in trades] == [1, -1]
assert trades[0]['entry_time'] == fixture.timestamp.iloc[2]
assert trades[0]['exit_time'] == fixture.timestamp.iloc[3]
assert trades[1]['entry_time'] == fixture.timestamp.iloc[3]
assert trades[1]['exit_time'] == fixture.timestamp.iloc[5]
print('PASS: draft date guards, direct reversal conditions, original Python next-open timing')
print('NOT RUN: Pine compilation, TradingView execution, real OHLCV parity, API orders')
