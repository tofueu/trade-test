"""Combine completed five-year strategy backtests with consistent IS-derived sizing."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import five_year_multi_market_kelly as base
ROOT=Path(__file__).resolve().parent
OOS=base.OOS

# Original single-indicator signals x every tested exit method. Recompute risk sizing
# exclusively from trades closed before OOS so all families use the same accounting.
ledger=pd.read_csv(ROOT/'five_year_exit_variants_ledger.csv')
ledger['entry_time']=pd.to_datetime(ledger.entry_time,utc=True)
ledger['exit_time']=pd.to_datetime(ledger.exit_time,utc=True)
keys=['市場','商品','代碼','訊號策略','出場方式']
original=[]
for key,g in ledger.groupby(keys,sort=False,dropna=False):
    g=g.sort_values('exit_time')
    allt=[{'R':float(x)} for x in g.R.dropna()]
    isg=g[(g.entry_time<OOS)&(g.exit_time<OOS)]
    oosg=g[g.entry_time>=OOS]
    ist=[{'R':float(x)} for x in isg.R.dropna()]
    oost=[{'R':float(x)} for x in oosg.R.dropna()]
    fs=base.formula_stats(ist)
    fk=max(0.,float(fs['kelly'])) if math.isfinite(fs['kelly']) else 0.
    counts=g.reason.value_counts().to_dict()
    tp=int(counts.get('止盈',0)+counts.get('ATR移動止盈',0))
    fixed_tp=int(counts.get('止盈',0))
    sl=int(counts.get('止損',0)+counts.get('ATR移動止損',0))
    for alloc,f in [('固定1R',.10),('全凱利',fk),('半凱利',fk/2),('四分之一凱利',fk/4)]:
        full=base.fixed_risk_stats(allt,f); op=base.fixed_risk_stats(oost,f)
        original.append({'測試類型':'原單指標×全部出場變體','市場':key[0],'商品':key[1],'代碼':key[2],
          '策略':key[3],'出場方式':key[4],'倉位法':alloc,'五年交易數':len(allt),'止盈出場數':tp,'固定止盈數':fixed_tp,'止損出場數':sl,
          '五年收益_pct':full[0],'五年最大回撤_pct':full[1],'OOS收益_pct':op[0],'OOS交易數':len(oost),
          'IS交易數':len(ist),'IS_Kelly_pct':fk*100})

# Previously generated compound and pure fixed-bracket tests.
comp=pd.read_csv(ROOT/'five_year_compound_is_selected_all.csv')
comp_rows=[]
for _,r in comp.iterrows():
    comp_rows.append({'測試類型':'雙指標／週線複合策略','市場':r['市場'],'商品':r['商品'],'代碼':r['代碼'],
      '策略':r['複合策略'],'策略規則':r['策略邏輯'],'出場方式':r['IS選定出場方式'],'倉位法':r['倉位方法'],
      '五年交易數':r['五年交易數'],'止盈出場數':r['止盈出場數'],'固定止盈數':r['固定止盈數'],'止損出場數':r['止損數'],
      '五年收益_pct':r['五年收益_pct'],'五年最大回撤_pct':r['五年最大回撤_pct'],
      'OOS收益_pct':r['OOS收益_pct'],'OOS交易數':r['OOS交易數'],'IS交易數':r['IS交易數'],'IS_Kelly_pct':r['IS_Kelly_pct']})
fixed=pd.read_csv(ROOT/'five_year_fixed_rr_low_drawdown_all.csv')
fixed_rows=[]
for _,r in fixed.iterrows():
    fixed_rows.append({'測試類型':'新指標策略×純固定盈虧','市場':r['市場'],'商品':r['商品'],'代碼':r['代碼'],
      '策略':r['策略'],'策略規則':r['策略規則'],'出場方式':f"純固定TP {r['止盈目標_R']}R／初始SL 1.5ATR",
      '倉位法':r['倉位法'],'五年交易數':r['五年交易數'],'止盈出場數':r['固定止盈數'],'固定止盈數':r['固定止盈數'],
      '止損出場數':r['止損數'],'五年收益_pct':r['五年收益_pct'],'五年最大回撤_pct':r['五年最大回撤_pct'],
      'OOS收益_pct':r['OOS收益_pct'],'OOS交易數':r['OOS交易數'],'IS交易數':r['IS交易數'],'IS_Kelly_pct':r['IS_Kelly_pct']})

allrows=pd.DataFrame(original+comp_rows+fixed_rows)
allrows=allrows.sort_values(['五年收益_pct','OOS收益_pct'],ascending=False).reset_index(drop=True)
allrows.insert(0,'綜合收益排名',np.arange(1,len(allrows)+1))
allrows.to_csv(ROOT/'all_completed_five_year_tests_ranked.csv',index=False,encoding='utf-8-sig')
allrows.head(50).to_csv(ROOT/'all_completed_five_year_tests_top50.csv',index=False,encoding='utf-8-sig')
pos=allrows[(allrows['五年收益_pct']>0)&(allrows['OOS收益_pct']>0)].copy().reset_index(drop=True)
pos.insert(0,'五年與OOS皆正收益排名',np.arange(1,len(pos)+1))
pos.to_csv(ROOT/'all_completed_five_year_tests_positive_oos.csv',index=False,encoding='utf-8-sig')
pos50=pos[pos['五年交易數']>50].sort_values('五年收益_pct',ascending=False).reset_index(drop=True)
pos50.insert(0,'正收益且超50筆排名',np.arange(1,len(pos50)+1))
pos50.to_csv(ROOT/'all_completed_five_year_tests_positive_oos_over50.csv',index=False,encoding='utf-8-sig')
print('COUNTS',len(original),len(comp_rows),len(fixed_rows),'TOTAL',len(allrows))
print('positive 5y',int((allrows['五年收益_pct']>0).sum()),'positive 5y+OOS',len(pos),'positive both and >50',len(pos50))
print('families',allrows['測試類型'].value_counts().to_dict())
print(allrows.head(50)[['綜合收益排名','測試類型','市場','商品','策略','出場方式','倉位法','五年交易數','止盈出場數','止損出場數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數']].to_string(index=False))
print('POS_OVER50_TOP20')
print(pos50.head(20)[['正收益且超50筆排名','測試類型','商品','策略','出場方式','倉位法','五年交易數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數']].to_string(index=False))
