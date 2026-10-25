"""Five-year backtest of two-indicator and higher-timeframe-confirmed strategies."""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd
import five_year_multi_market_kelly as base
import five_year_exit_method_sweep as exits

ROOT=Path(__file__).resolve().parent
OOS=base.OOS

DEFINITIONS={
 'EMA200+RSI14_pullback':'日線EMA200定方向；RSI14由30上穿做多（EMA200上方），由70下穿做空（EMA200下方）；EMA200/RSI退出條件平倉。',
 'EMA200+RSI2_mean_reversion':'日線EMA200定方向；RSI2<10在EMA200上方做多，RSI2>90在下方做空；RSI2回到70/30或EMA200失守出場。',
 'Donchian20+MACD':'日線收盤突破前20日高/低，且MACD方向一致才進場；跌破/突破前10日反向通道或MACD反向時退出。',
 'MACD+RSI50':'日線MACD與訊號線方向一致，且RSI14同時在50上/下方才持倉；任一方向條件失效即退場。',
 'Supertrend+EMA200':'日線Supertrend翻多/空且收盤同時位於EMA200上/下才持倉；方向不再一致即退出。',
 'Supertrend+RSI50':'日線Supertrend方向與RSI14的50線方向一致才持倉；任一條件失效即退出。',
 'WEMA20_50+Donchian20':'以前一個完整週線的EMA20/EMA50判斷大方向；日線突破前20日高/低且方向與週線一致才進場，日線10日反向通道或週線方向變更則退出。',
 'WEMA20_50+MACD':'以前一個完整週線的EMA20/EMA50確認大方向；日線MACD交叉順週線方向進場，MACD反向或週線方向變更則退出。',
}

def custom_signals(d:pd.DataFrame, name:str)->np.ndarray:
    c=d.close.to_numpy(); n=len(d); sig=np.zeros(n,dtype=np.int8); state=0
    rsi14=d.rsi14.to_numpy(); rsi2=d.rsi2.to_numpy(); e200=d.ema200.to_numpy()
    macd=d.macd.to_numpy(); ms=d.macdsig.to_numpy(); st=d.st_dir.to_numpy()
    # Weekly EMA trend; assign only the previous completed weekly bucket to daily bars.
    weekly=d.set_index('timestamp')['close'].resample('W-SUN').last().dropna()
    we20=weekly.ewm(span=20,adjust=False,min_periods=20).mean()
    we50=weekly.ewm(span=50,adjust=False,min_periods=50).mean()
    wreg=np.sign(we20-we50).fillna(0).astype(np.int8)
    wreg.index=weekly.index.tz_localize(None).to_period('W-SUN')
    wreg=wreg.shift(1).fillna(0).astype(np.int8)
    wkkey=d.timestamp.dt.tz_localize(None).dt.to_period('W-SUN')
    wr=wkkey.map(wreg).fillna(0).to_numpy(dtype=np.int8)
    for i in range(n):
      prev_i=max(0,i-1); nxt=state
      if name=='EMA200+RSI14_pullback':
        if i and c[i]>e200[i] and rsi14[prev_i]<=30<rsi14[i]: nxt=1
        elif i and c[i]<e200[i] and rsi14[prev_i]>=70>rsi14[i]: nxt=-1
        elif state==1 and (c[i]<e200[i] or rsi14[i]>=60): nxt=0
        elif state==-1 and (c[i]>e200[i] or rsi14[i]<=40): nxt=0
      elif name=='EMA200+RSI2_mean_reversion':
        if c[i]>e200[i] and rsi2[i]<10: nxt=1
        elif c[i]<e200[i] and rsi2[i]>90: nxt=-1
        elif state==1 and (c[i]<e200[i] or rsi2[i]>70): nxt=0
        elif state==-1 and (c[i]>e200[i] or rsi2[i]<30): nxt=0
      elif name=='Donchian20+MACD':
        if c[i]>d.hi20.iat[i] and macd[i]>ms[i]: nxt=1
        elif c[i]<d.lo20.iat[i] and macd[i]<ms[i]: nxt=-1
        elif state==1 and (c[i]<d.lo10.iat[i] or macd[i]<ms[i]): nxt=0
        elif state==-1 and (c[i]>d.hi10.iat[i] or macd[i]>ms[i]): nxt=0
      elif name=='MACD+RSI50':
        if macd[i]>ms[i] and rsi14[i]>50: nxt=1
        elif macd[i]<ms[i] and rsi14[i]<50: nxt=-1
        elif state==1 and (macd[i]<=ms[i] or rsi14[i]<=50): nxt=0
        elif state==-1 and (macd[i]>=ms[i] or rsi14[i]>=50): nxt=0
      elif name=='Supertrend+EMA200':
        if st[i]>0 and c[i]>e200[i]: nxt=1
        elif st[i]<0 and c[i]<e200[i]: nxt=-1
        else: nxt=0
      elif name=='Supertrend+RSI50':
        if st[i]>0 and rsi14[i]>50: nxt=1
        elif st[i]<0 and rsi14[i]<50: nxt=-1
        else: nxt=0
      elif name=='WEMA20_50+Donchian20':
        if wr[i]>0 and c[i]>d.hi20.iat[i]: nxt=1
        elif wr[i]<0 and c[i]<d.lo20.iat[i]: nxt=-1
        elif state==1 and (wr[i]<=0 or c[i]<d.lo10.iat[i]): nxt=0
        elif state==-1 and (wr[i]>=0 or c[i]>d.hi10.iat[i]): nxt=0
      elif name=='WEMA20_50+MACD':
        if wr[i]>0 and i and macd[i]>ms[i] and macd[prev_i]<=ms[prev_i]: nxt=1
        elif wr[i]<0 and i and macd[i]<ms[i] and macd[prev_i]>=ms[prev_i]: nxt=-1
        elif state==1 and (wr[i]<=0 or macd[i]<ms[i]): nxt=0
        elif state==-1 and (wr[i]>=0 or macd[i]>ms[i]): nxt=0
      sig[i]=nxt; state=nxt
    return sig

# Exit sweep calls the regular signal interface. Override it only inside this process.
base.make_signals=custom_signals

instruments=[]
for s in base.CRYPTO: instruments.append(('Crypto futures',s,s,lambda s=s:base.binance_daily(s)))
for s,(name,_) in base.FX.items(): instruments.append(('FX',s,name,lambda s=s:base.yahoo_daily(s)))
for s,(name,_,_) in base.FUTURES.items(): instruments.append(('Traditional futures',s,name,lambda s=s:base.yahoo_daily(s)))
rows=[]; ledger=[]
for market,symbol,label,loader in instruments:
    raw=loader().dropna(subset=['open','high','low','close']).copy()
    raw['timestamp']=pd.to_datetime(raw.timestamp,utc=True)
    raw=raw.sort_values('timestamp').drop_duplicates('timestamp').reset_index(drop=True)
    for strategy in DEFINITIONS:
      for mode,tp,trail in exits.MODES:
        ts=exits.backtest(raw,market,symbol,strategy,tp,trail)
        if not ts: continue
        g=[t for t in ts]
        is_closed=[t for t in g if pd.Timestamp(t['entry_time'])<OOS and pd.Timestamp(t['exit_time'])<OOS]
        # Exit selection: 10% of initial equity risk, chosen only from closed IS trades.
        isret=base.fixed_risk_stats(is_closed,.10)[0]
        for t in g: ledger.append({'市場':market,'商品':label,'代碼':symbol,'複合策略':strategy,'出場方式':mode,**t})
        rows.append({'市場':market,'商品':label,'代碼':symbol,'複合策略':strategy,'策略邏輯':DEFINITIONS[strategy],
                     '出場方式':mode,'交易數':len(g),'IS已平倉數':len(is_closed),'IS固定1R收益_pct':isret,
                     'trades':g})
    print('DONE',market,label,flush=True)

# Choose each market/strategy exit using only the first four years.
selected=[]
for (market,label,symbol,strategy), group in pd.DataFrame(rows).groupby(['市場','商品','代碼','複合策略'],sort=False):
    best=group.sort_values(['IS固定1R收益_pct','IS已平倉數','出場方式'],ascending=[False,False,True]).iloc[0]
    trades=best.trades
    is_tr=[t for t in trades if pd.Timestamp(t['entry_time'])<OOS and pd.Timestamp(t['exit_time'])<OOS]
    oos_tr=[t for t in trades if pd.Timestamp(t['entry_time'])>=OOS]
    all_tr=trades
    fs=base.formula_stats(is_tr)
    fk=max(0.,fs['kelly']) if math.isfinite(fs['kelly']) else 0.
    counts={r:sum(t['reason']==r for t in all_tr) for r in ['止盈','止損','訊號出場','ATR移動止盈','ATR移動止損','期末平倉']}
    for allocation,f in [('固定1R',.10),('全凱利',fk),('半凱利',fk/2),('四分之一凱利',fk/4)]:
      full=base.fixed_risk_stats(all_tr,f); isperf=base.fixed_risk_stats(is_tr,f); op=base.fixed_risk_stats(oos_tr,f)
      selected.append({'市場':market,'商品':label,'代碼':symbol,'複合策略':strategy,'策略邏輯':DEFINITIONS[strategy],
        'IS選定出場方式':best.出場方式,'倉位方法':allocation,'IS選出場固定1R收益_pct':best.IS固定1R收益_pct,
        'IS交易數':len(is_tr),'五年交易數':len(all_tr),'止盈出場數':counts['止盈']+counts['ATR移動止盈'],
        '固定止盈數':counts['止盈'],'ATR移動止盈數':counts['ATR移動止盈'],'止損數':counts['止損']+counts['ATR移動止損'],
        '訊號出場數':counts['訊號出場'],'期末平倉數':counts['期末平倉'],
        '五年收益_pct':full[0],'五年最大回撤_pct':full[1],'IS收益_pct':isperf[0],
        'OOS收益_pct':op[0],'OOS最大回撤_pct':op[1],'OOS交易數':len(oos_tr),
        'IS_Kelly_pct':fk*100,'IS勝率_pct':fs['p']*100 if math.isfinite(fs['p']) else np.nan,'IS平均R':fs['ev']})
    for j,t in enumerate(all_tr,1): ledger.append({'市場':market,'商品':label,'代碼':symbol,'複合策略':strategy,'出場方式':best.出場方式,'trade_no':j,**t})

out=pd.DataFrame(selected).sort_values('五年收益_pct',ascending=False).reset_index(drop=True)
out.insert(0,'五年收益排名',np.arange(1,len(out)+1))
out.to_csv(ROOT/'five_year_compound_is_selected_all.csv',index=False,encoding='utf-8-sig')
out.head(50).to_csv(ROOT/'five_year_compound_is_selected_top50.csv',index=False,encoding='utf-8-sig')
over=out[(out.五年交易數>50)&(out.五年收益_pct>0)&(out.OOS收益_pct>0)].sort_values('五年收益_pct',ascending=False).reset_index(drop=True)
over.insert(0,'正收益且超50筆子榜排名',np.arange(1,len(over)+1))
over.to_csv(ROOT/'five_year_compound_positive_over50.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(ledger).to_csv(ROOT/'five_year_compound_trade_ledger.csv',index=False,encoding='utf-8-sig')
print('COMPOUND_ROWS',len(out),'positive 5y',int((out.五年收益_pct>0).sum()),'positive OOS',int((out.OOS收益_pct>0).sum()),'over50 positive both',len(over))
print(out.head(30)[['五年收益排名','商品','複合策略','IS選定出場方式','倉位方法','五年交易數','止盈出場數','止損數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數']].to_string(index=False))
print('OVER50')
print(over.head(20)[['正收益且超50筆子榜排名','商品','複合策略','IS選定出場方式','倉位方法','五年交易數','止盈出場數','五年收益_pct','OOS收益_pct','OOS交易數']].to_string(index=False))
