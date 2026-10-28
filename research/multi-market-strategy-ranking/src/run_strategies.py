"""Test additional trend, breakout, and mean-reversion strategies with fixed TP/SL.

Signals use completed daily bars and enter at the next open. Stops are 1.5 ATR;
TP candidates are selected on the first four years by return/drawdown, then
reported on the full five years and final-year OOS.
"""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import five_year_multi_market_kelly as base

ROOT=Path(__file__).resolve().parent
TP_RS=[0.75,1.0,1.5,2.0,3.0]
RULES={
 'Turtle55_20_EMA200':'55日通道突破進場，EMA200 同方向過濾；反向 20 日通道突破出場。',
 'Supertrend_ADX20':'Supertrend(10,3) 翻向且 ADX14>20 才進場；Supertrend 反向即退出。',
 'EMA20_50_ADX20':'EMA20/EMA50 黃金交叉或死亡交叉，且 ADX14>20 才進場；反向交叉退出。',
 'Keltner20_1.5ATR_EMA200':'收盤突破 EMA20±1.5ATR 通道，並符合 EMA200 趨勢方向；收盤回到 EMA20 另一側退出。',
 'BB_Reentry_RSI_ADX25':'低於 ADX25 時，收盤從布林 2σ 外回到帶內且 RSI14<45 做多／RSI14>55 做空；回到中軌退出。',
 'Donchian20_Volume_EMA200':'成交量高於 20 日均量 1.5 倍時突破 20 日通道，並符合 EMA200 方向；反向突破 10 日通道退出。',
 'MACD_EMA200_ADX20':'ADX14>20 時 MACD 訊號交叉且價格符合 EMA200 趨勢方向進場；反向 MACD 交叉或趨勢失效退出。',
}

def add_adx(d):
    up=d.high.diff(); down=-d.low.diff()
    plus=up.where((up>down)&(up>0),0.0); minus=down.where((down>up)&(down>0),0.0)
    prev=d.close.shift(1)
    tr=pd.concat([d.high-d.low,(d.high-prev).abs(),(d.low-prev).abs()],axis=1).max(axis=1)
    atr=tr.ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    pdi=100*plus.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
    mdi=100*minus.ewm(alpha=1/14,adjust=False,min_periods=14).mean()/atr.replace(0,np.nan)
    dx=100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)
    d['adx14']=dx.ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    d['hi55']=d.high.shift(1).rolling(55,min_periods=55).max(); d['lo55']=d.low.shift(1).rolling(55,min_periods=55).min()
    d['hi10x']=d.high.shift(1).rolling(10,min_periods=10).max(); d['lo10x']=d.low.shift(1).rolling(10,min_periods=10).min()
    d['hi20x']=d.high.shift(1).rolling(20,min_periods=20).max(); d['lo20x']=d.low.shift(1).rolling(20,min_periods=20).min()
    d['ema20']=d.close.ewm(span=20,adjust=False).mean()
    d['volsma20x']=d.volume.rolling(20,min_periods=20).mean()
    return d

def make_state(d,name):
    n=len(d); c=d.close.to_numpy(); state=0; sig=np.zeros(n,dtype=np.int8)
    for i in range(1,n):
        row=d.iloc[i]; prev=d.iloc[i-1]; nxt=state
        if name=='Turtle55_20_EMA200':
            if c[i]>row.hi55 and c[i]>row.ema200: nxt=1
            elif c[i]<row.lo55 and c[i]<row.ema200: nxt=-1
            elif state==1 and c[i]<row.lo20x: nxt=0
            elif state==-1 and c[i]>row.hi20x: nxt=0
        elif name=='Supertrend_ADX20':
            if prev.st_dir<=0<row.st_dir and row.adx14>20: nxt=1
            elif prev.st_dir>=0>row.st_dir and row.adx14>20: nxt=-1
            elif state==1 and row.st_dir<0: nxt=0
            elif state==-1 and row.st_dir>0: nxt=0
        elif name=='EMA20_50_ADX20':
            if prev.ema20<=prev.ema50 and row.ema20>row.ema50 and row.adx14>20: nxt=1
            elif prev.ema20>=prev.ema50 and row.ema20<row.ema50 and row.adx14>20: nxt=-1
        elif name=='Keltner20_1.5ATR_EMA200':
            upper=row.ema20+1.5*row.atr; lower=row.ema20-1.5*row.atr
            if c[i]>upper and c[i]>row.ema200: nxt=1
            elif c[i]<lower and c[i]<row.ema200: nxt=-1
            elif state==1 and c[i]<row.ema20: nxt=0
            elif state==-1 and c[i]>row.ema20: nxt=0
        elif name=='BB_Reentry_RSI_ADX25':
            if prev.close<=prev.bblow and c[i]>row.bblow and row.rsi14<45 and row.adx14<25: nxt=1
            elif prev.close>=prev.bbhi and c[i]<row.bbhi and row.rsi14>55 and row.adx14<25: nxt=-1
            elif state==1 and c[i]>=row.bbmid: nxt=0
            elif state==-1 and c[i]<=row.bbmid: nxt=0
        elif name=='Donchian20_Volume_EMA200':
            vok=pd.notna(row.volsma20x) and row.volume>1.5*row.volsma20x
            if vok and c[i]>row.hi20x and c[i]>row.ema200: nxt=1
            elif vok and c[i]<row.lo20x and c[i]<row.ema200: nxt=-1
            elif state==1 and c[i]<row.lo10x: nxt=0
            elif state==-1 and c[i]>row.hi10x: nxt=0
        elif name=='MACD_EMA200_ADX20':
            if row.adx14>20 and c[i]>row.ema200 and prev.macd<=prev.macdsig and row.macd>row.macdsig: nxt=1
            elif row.adx14>20 and c[i]<row.ema200 and prev.macd>=prev.macdsig and row.macd<row.macdsig: nxt=-1
            elif state==1 and (c[i]<row.ema200 or row.macd<row.macdsig): nxt=0
            elif state==-1 and (c[i]>row.ema200 or row.macd>row.macdsig): nxt=0
        sig[i]=nxt; state=nxt
    return sig

def run(raw,market,symbol,name,tp_r):
    d=add_adx(base.indicators(raw)); sig=make_state(d,name); slip,fee=base.costs(market,symbol)
    o,h,l,c,atr=(d[x].to_numpy() for x in ['open','high','low','close','atr']); ts=d.timestamp
    trades=[]; side=0; entry=stop=take=dist=0.; entry_i=0
    def slipamt(px): return slip*abs(px) if market=='Crypto futures' else slip
    for i in range(1,len(d)):
        if ts.iloc[i]<base.START: continue
        target=int(sig[i-1])
        if side and target!=side:
            ex=o[i]-side*slipamt(o[i]); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
            trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[i],'R':pnl/dist if dist else 0.,'reason':'訊號出場'}); side=0
        elif side:
            slhit=(o[i]<=stop or l[i]<=stop) if side==1 else (o[i]>=stop or h[i]>=stop)
            tphit=(o[i]>=take or h[i]>=take) if side==1 else (o[i]<=take or l[i]<=take)
            if slhit or tphit:
                if slhit: px=min(o[i],stop) if side==1 else max(o[i],stop); reason='止損'
                else: px=take; reason='止盈'
                ex=px-side*slipamt(px); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
                trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[i],'R':pnl/dist if dist else 0.,'reason':reason}); side=0
        if not side and target and (i==1 or sig[i-2]==0 or target!=int(sig[i-2])) and np.isfinite(atr[i-1]) and atr[i-1]>0:
            side=target; entry_i=i; entry=o[i]+side*slipamt(o[i]); dist=1.5*atr[i-1]; stop=entry-side*dist; take=entry+side*tp_r*dist
            slhit=(l[i]<=stop if side==1 else h[i]>=stop); tphit=(h[i]>=take if side==1 else l[i]<=take)
            if slhit or tphit:
                if slhit: px=min(o[i],stop) if side==1 else max(o[i],stop); reason='止損'
                else: px=take; reason='止盈'
                ex=px-side*slipamt(px); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
                trades.append({'entry_time':ts.iloc[i],'exit_time':ts.iloc[i],'R':pnl/dist if dist else 0.,'reason':reason}); side=0
    if side:
        ex=c[-1]-side*slipamt(c[-1]); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex))
        trades.append({'entry_time':ts.iloc[entry_i],'exit_time':ts.iloc[-1],'R':pnl/dist if dist else 0.,'reason':'期末平倉'})
    return trades

def main():
    instruments=[]
    for s in base.CRYPTO: instruments.append(('Crypto futures',s,s,base.binance_daily(s)))
    for s,(label,_) in base.FX.items(): instruments.append(('FX',s,label,base.yahoo_daily(s)))
    for s,(label,_,_) in base.FUTURES.items(): instruments.append(('Traditional futures',s,label,base.yahoo_daily(s)))
    rows=[]
    for market,symbol,label,raw in instruments:
        raw=raw.dropna(subset=['open','high','low','close']).sort_values('timestamp').drop_duplicates('timestamp').reset_index(drop=True)
        for name in RULES:
            variants=[]
            for tp in TP_RS:
                tr=run(raw,market,symbol,name,tp)
                is_tr=[t for t in tr if pd.Timestamp(t['entry_time'])<base.OOS and pd.Timestamp(t['exit_time'])<base.OOS]
                ret,dd,_,_=base.fixed_risk_stats(is_tr,.10)
                variants.append((tp,tr,is_tr,ret,dd))
            eligible=[x for x in variants if len(x[2])>=20 and x[3]>0]
            if not eligible: eligible=[x for x in variants if x[3]>0]
            if not eligible: eligible=variants
            chosen=max(eligible,key=lambda x:(x[3]/max(x[4],1.),x[3],len(x[2])))
            tp,tr,is_tr,isret,isdd=chosen
            oos_tr=[t for t in tr if pd.Timestamp(t['entry_time'])>=base.OOS]
            fk=base.formula_stats(is_tr)['kelly']; fk=max(0.,float(fk)) if math.isfinite(fk) else 0.
            cnt=pd.Series([t['reason'] for t in tr]).value_counts().to_dict()
            for alloc,f in [('固定1R',.10),('全凱利',fk),('半凱利',fk/2),('四分之一凱利',fk/4)]:
                full=base.fixed_risk_stats(tr,f); oos=base.fixed_risk_stats(oos_tr,f)
                rows.append({'測試類型':'新增趨勢／突破／均值回歸×固定TP/SL','市場':market,'商品':label,'代碼':symbol,
                  '策略':name,'策略規則':RULES[name],'出場方式':f'IS選定固定TP {tp:g}R／初始SL 1.5ATR＋策略出場',
                  '倉位法':alloc,'五年交易數':len(tr),'止盈出場數':int(cnt.get('止盈',0)),
                  '固定止盈數':int(cnt.get('止盈',0)),'止損出場數':int(cnt.get('止損',0)),
                  '五年收益_pct':full[0],'五年最大回撤_pct':full[1],'OOS收益_pct':oos[0],
                  'OOS交易數':len(oos_tr),'IS交易數':len(is_tr),'IS_Kelly_pct':fk*100})
        print('DONE',market,label,flush=True)
    df=pd.DataFrame(rows).sort_values('五年收益_pct',ascending=False).reset_index(drop=True)
    df.insert(0,'新增策略排名',np.arange(1,len(df)+1))
    df.to_csv(ROOT/'additional_fixed_rr_results.csv',index=False,encoding='utf-8-sig')
    df.head(50).to_csv(ROOT/'additional_fixed_rr_top50.csv',index=False,encoding='utf-8-sig')
    print('COUNT',len(df),'positive both',int(((df['五年收益_pct']>0)&(df['OOS收益_pct']>0)).sum()))
    print(df.head(20)[['新增策略排名','商品','策略','出場方式','倉位法','五年交易數','固定止盈數','止損出場數','五年收益_pct','五年最大回撤_pct','OOS收益_pct','OOS交易數']].to_string(index=False))

if __name__=='__main__': main()
