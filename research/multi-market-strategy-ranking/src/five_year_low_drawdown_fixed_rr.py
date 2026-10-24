"""Candidate composite systems with fixed ATR stop and fixed R targets."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import five_year_multi_market_kelly as base
ROOT=Path(__file__).resolve().parent
TP_RS=[0.5,1.0,1.5,2.0,3.0]

RULES={
'EMA200+RSI14_pullback':'日線 EMA200 定方向；RSI14 由 30 上穿才做多（價在 EMA200 上），由 70 下穿才做空（價在 EMA200 下）。',
'EMA200+RSI2_extreme':'日線 EMA200 定方向；RSI2 向下穿越 10 做多（價在 EMA200 上），向上穿越 90 做空（價在 EMA200 下）。',
'EMA200+MACD_cross':'日線收盤在 EMA200 上方且 MACD 上穿訊號線做多；在下方且 MACD 下穿做空。',
'Donchian20+ADX14':'日線收盤突破前 20 日高／低，且 ADX14>20 才順向進場。',
'Bollinger20+RSI14_reentry':'收盤由布林 2σ 下軌外回到軌內且 RSI14<45 做多；上軌外回到軌內且 RSI14>55 做空。',
'Supertrend+EMA200_flip':'日線 Supertrend(ATR10,3) 翻多且收盤在 EMA200 上做多；翻空且收盤在 EMA200 下做空。',
'WEMA20_50+DailyMACD':'以前一個已完成週線 EMA20/EMA50 定方向；日線 MACD 順週線方向交叉進場。',
'WEMA20_50+DailyDonchian20':'以前一個已完成週線 EMA20/EMA50 定方向；日線收盤突破前 20 日高／低進場。',
'Stoch14+EMA200':'日線 EMA200 定方向；%K(14) 上穿 20 做多（價在 EMA200 上），下穿 80 做空（價在 EMA200 下）。',
}

def signals(d,name):
 c=d.close.to_numpy(); n=len(d); s=np.zeros(n,dtype=np.int8)
 e200=d.ema200.to_numpy(); m=d.macd.to_numpy(); ms=d.macdsig.to_numpy(); r14=d.rsi14.to_numpy(); r2=d.rsi2.to_numpy(); st=d.st_dir.to_numpy()
 hi20=d.hi20.to_numpy(); lo20=d.lo20.to_numpy(); bblo=d.bblow.to_numpy(); bbhi=d.bbhi.to_numpy()
 # ADX14 from Wilder-smoothed directional movement and true range.
 up=d.high.diff(); down=-d.low.diff()
 plus_dm=up.where((up>down)&(up>0),0.0); minus_dm=down.where((down>up)&(down>0),0.0)
 prev=d.close.shift(1); tr=pd.concat([d.high-d.low,(d.high-prev).abs(),(d.low-prev).abs()],axis=1).max(axis=1)
 atr=tr.ewm(alpha=1/14,adjust=False,min_periods=14).mean()
 pdi=100*plus_dm.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
 mdi=100*minus_dm.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
 dx=100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan); adx=dx.ewm(alpha=1/14,adjust=False,min_periods=14).mean().to_numpy()
 # stochastic %K(14)
 low14=d.low.rolling(14,min_periods=14).min(); high14=d.high.rolling(14,min_periods=14).max()
 k=(100*(d.close-low14)/(high14-low14).replace(0,np.nan)).to_numpy()
 # Previous fully completed week only (no current-week look-ahead).
 weekly=d.set_index('timestamp')['close'].resample('W-SUN').last().dropna()
 w20=weekly.ewm(span=20,adjust=False,min_periods=20).mean(); w50=weekly.ewm(span=50,adjust=False,min_periods=50).mean()
 wr=np.sign(w20-w50).fillna(0).astype(np.int8); wr.index=weekly.index.tz_localize(None).to_period('W-SUN')
 wr=wr.shift(1).fillna(0).astype(np.int8)
 wk=d.timestamp.dt.tz_localize(None).dt.to_period('W-SUN'); wtrend=wk.map(wr).fillna(0).to_numpy(dtype=np.int8)
 for i in range(1,n):
  p=i-1
  if name=='EMA200+RSI14_pullback':
   if c[i]>e200[i] and r14[p]<=30<r14[i]: s[i]=1
   elif c[i]<e200[i] and r14[p]>=70>r14[i]: s[i]=-1
  elif name=='EMA200+RSI2_extreme':
   if c[i]>e200[i] and r2[p]>=10>r2[i]: s[i]=1
   elif c[i]<e200[i] and r2[p]<=90<r2[i]: s[i]=-1
  elif name=='EMA200+MACD_cross':
   if c[i]>e200[i] and m[p]<=ms[p] and m[i]>ms[i]: s[i]=1
   elif c[i]<e200[i] and m[p]>=ms[p] and m[i]<ms[i]: s[i]=-1
  elif name=='Donchian20+ADX14':
   if c[p]<=hi20[p] and c[i]>hi20[i] and adx[i]>20: s[i]=1
   elif c[p]>=lo20[p] and c[i]<lo20[i] and adx[i]>20: s[i]=-1
  elif name=='Bollinger20+RSI14_reentry':
   if c[p]<=bblo[p] and c[i]>bblo[i] and r14[i]<45: s[i]=1
   elif c[p]>=bbhi[p] and c[i]<bbhi[i] and r14[i]>55: s[i]=-1
  elif name=='Supertrend+EMA200_flip':
   if st[p]<=0<st[i] and c[i]>e200[i]: s[i]=1
   elif st[p]>=0>st[i] and c[i]<e200[i]: s[i]=-1
  elif name=='WEMA20_50+DailyMACD':
   if wtrend[i]>0 and m[p]<=ms[p] and m[i]>ms[i]: s[i]=1
   elif wtrend[i]<0 and m[p]>=ms[p] and m[i]<ms[i]: s[i]=-1
  elif name=='WEMA20_50+DailyDonchian20':
   if wtrend[i]>0 and c[p]<=hi20[p] and c[i]>hi20[i]: s[i]=1
   elif wtrend[i]<0 and c[p]>=lo20[p] and c[i]<lo20[i]: s[i]=-1
  elif name=='Stoch14+EMA200':
   if c[i]>e200[i] and k[p]<=20<k[i]: s[i]=1
   elif c[i]<e200[i] and k[p]>=80>k[i]: s[i]=-1
 return s

def run_bracket(raw,market,symbol,name,tp_r):
 d=base.indicators(raw); sig=signals(d,name)
 slip,fee=base.costs(market,symbol)
 def slipamt(px): return slip*abs(px) if market=='Crypto futures' else slip
 o,h,l,c=d.open.to_numpy(),d.high.to_numpy(),d.low.to_numpy(),d.close.to_numpy(); atr=d.atr.to_numpy(); ts=d.timestamp
 side=0; entry=stop=take=dist=0.; entry_i=0; trades=[]
 for i in range(1,len(d)):
  if ts.iloc[i]<base.START: continue
  if side:
   slhit=(o[i]<=stop or l[i]<=stop) if side==1 else (o[i]>=stop or h[i]>=stop)
   tphit=(o[i]>=take or h[i]>=take) if side==1 else (o[i]<=take or l[i]<=take)
   if slhit or tphit:
    # If both levels are reached in one daily bar, assume stop first.
    if slhit:
     px=min(o[i],stop) if side==1 else max(o[i],stop); reason='止損'
    else: px=take; reason='固定止盈'
    ex=px-side*slipamt(px); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
    trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[i],'side':side,'R':pnl/dist if dist else 0.,'reason':reason})
    side=0
  if not side and sig[i-1]!=0 and np.isfinite(atr[i-1]) and atr[i-1]>0:
   side=int(sig[i-1]); entry_i=i; entry=o[i]+side*slipamt(o[i]); dist=1.5*atr[i-1]
   stop=entry-side*dist; take=entry+side*tp_r*dist
   slhit=(l[i]<=stop if side==1 else h[i]>=stop)
   tphit=(h[i]>=take if side==1 else l[i]<=take)
   if slhit or tphit:
    if slhit: px=min(o[i],stop) if side==1 else max(o[i],stop); reason='止損'
    else: px=take; reason='固定止盈'
    ex=px-side*slipamt(px); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
    trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[i],'side':side,'R':pnl/dist if dist else 0.,'reason':reason}); side=0
 if side:
  px=c[-1]; ex=px-side*slipamt(px); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
  trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[-1],'side':side,'R':pnl/dist if dist else 0.,'reason':'期末平倉'})
 return trades

instruments=[]
for s in base.CRYPTO: instruments.append(('Crypto futures',s,s,lambda s=s:base.binance_daily(s)))
for s,(label,_) in base.FX.items(): instruments.append(('FX',s,label,lambda s=s:base.yahoo_daily(s)))
for s,(label,_,_) in base.FUTURES.items(): instruments.append(('Traditional futures',s,label,lambda s=s:base.yahoo_daily(s)))
rawrows=[]
for market,symbol,label,loader in instruments:
 raw=loader().dropna(subset=['open','high','low','close']).copy(); raw['timestamp']=pd.to_datetime(raw.timestamp,utc=True)
 raw=raw.sort_values('timestamp').drop_duplicates('timestamp').reset_index(drop=True)
 for strat in RULES:
  for tp in TP_RS:
   tr=run_bracket(raw,market,symbol,strat,tp)
   if tr:
    is_tr=[x for x in tr if pd.Timestamp(x['entry_time'])<base.OOS and pd.Timestamp(x['exit_time'])<base.OOS]
    oos_tr=[x for x in tr if pd.Timestamp(x['entry_time'])>=base.OOS]
    isret,isdd,isn,_=base.fixed_risk_stats(is_tr,.10)
    rawrows.append({'市場':market,'商品':label,'代碼':symbol,'策略':strat,'固定TP_R':tp,'trades':tr,'IS交易數':len(is_tr),'IS固定1R收益_pct':isret,'IS固定1R回撤_pct':isdd})
 print('DONE',market,label,flush=True)

# Choose target R by IS Calmar proxy among profitable, adequately sampled variants.
allrows=[]
rawdf=pd.DataFrame(rawrows)
for (market,label,symbol,strat),g in rawdf.groupby(['市場','商品','代碼','策略'],sort=False):
 viable=g[(g.IS交易數>=20)&(g.IS固定1R收益_pct>0)].copy()
 if viable.empty: viable=g[g.IS固定1R收益_pct>0].copy()
 if viable.empty: viable=g.copy()
 viable['IS_Return_DD']=viable.IS固定1R收益_pct/viable.IS固定1R回撤_pct.clip(lower=1.0)
 best=viable.sort_values(['IS_Return_DD','IS固定1R收益_pct','IS交易數'],ascending=False).iloc[0]
 tr=best.trades; is_tr=[x for x in tr if pd.Timestamp(x['entry_time'])<base.OOS and pd.Timestamp(x['exit_time'])<base.OOS]; oos_tr=[x for x in tr if pd.Timestamp(x['entry_time'])>=base.OOS]
 fs=base.formula_stats(is_tr); fk=max(0.,fs['kelly']) if math.isfinite(fs['kelly']) else 0.
 counts={r:sum(x['reason']==r for x in tr) for r in ['固定止盈','止損','期末平倉']}
 for alloc,f in [('固定1R',.10),('全凱利',fk),('半凱利',fk/2),('四分之一凱利',fk/4)]:
  fr=base.fixed_risk_stats(tr,f); ir=base.fixed_risk_stats(is_tr,f); oo=base.fixed_risk_stats(oos_tr,f)
  allrows.append({'市場':market,'商品':label,'代碼':symbol,'策略':strat,'策略規則':RULES[strat],'止盈目標_R':best.固定TP_R,'倉位法':alloc,
   'IS交易數':len(is_tr),'五年交易數':len(tr),'固定止盈數':counts['固定止盈'],'止損數':counts['止損'],'期末平倉數':counts['期末平倉'],
   'IS固定1R收益_pct':best.IS固定1R收益_pct,'IS固定1R回撤_pct':best.IS固定1R回撤_pct,'五年收益_pct':fr[0],'五年最大回撤_pct':fr[1],
   'IS收益_pct':ir[0],'OOS收益_pct':oo[0],'OOS最大回撤_pct':oo[1],'OOS交易數':len(oos_tr),'IS_Kelly_pct':fk*100,'IS勝率_pct':fs['p']*100 if math.isfinite(fs['p']) else np.nan})
out=pd.DataFrame(allrows).sort_values(['五年最大回撤_pct','五年收益_pct'],ascending=[True,False]).reset_index(drop=True)
out.insert(0,'低回撤排名',np.arange(1,len(out)+1))
out.to_csv(ROOT/'five_year_fixed_rr_low_drawdown_all.csv',index=False,encoding='utf-8-sig')
pos=out[(out['五年收益_pct']>0)&(out['OOS收益_pct']>0)].copy().sort_values(['五年最大回撤_pct','五年收益_pct'],ascending=[True,False]).reset_index(drop=True)
pos.insert(0,'正收益低回撤排名',np.arange(1,len(pos)+1))
pos.to_csv(ROOT/'five_year_fixed_rr_positive_low_drawdown.csv',index=False,encoding='utf-8-sig')
over=pos[pos['五年交易數']>50].reset_index(drop=True); over.insert(0,'正收益且超50筆排名',np.arange(1,len(over)+1))
over.to_csv(ROOT/'five_year_fixed_rr_positive_over50.csv',index=False,encoding='utf-8-sig')
print('TOTAL',len(out),'positive 5y+OOS',len(pos),'over50',len(over))
print('LOW_DD positive over50')
print(over.head(30)[['正收益且超50筆排名','商品','策略','止盈目標_R','倉位法','五年交易數','固定止盈數','止損數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數']].to_string(index=False))
print('RETURN/DD top positive over50')
rr=over.assign(ReturnDD=over['五年收益_pct']/over['五年最大回撤_pct'].clip(lower=1)).sort_values('ReturnDD',ascending=False)
print(rr.head(20)[['商品','策略','止盈目標_R','倉位法','五年交易數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數','ReturnDD']].to_string(index=False))
