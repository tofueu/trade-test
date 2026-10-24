"""Five-year multi-market daily strategy/Kelly comparison.

Public data: Binance USD-M monthly daily klines and Yahoo Finance chart history
for FX/futures continuous symbols. This is a research backtest, not execution.
"""
from __future__ import annotations
import io, json, math, time, urllib.parse, urllib.request, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "five_year_market_data"
CACHE.mkdir(exist_ok=True)
START = pd.Timestamp("2021-10-10", tz="UTC")
WARM = pd.Timestamp("2021-07-01", tz="UTC")
END = pd.Timestamp("2026-10-10", tz="UTC")
OOS = pd.Timestamp("2025-10-10", tz="UTC")
INITIAL = 10_000.0
FIXED_RISK = 0.10  # consistent with prior lecture example: 1R = $1,000 on $10,000
CRYPTO = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
FX = {
    "EURUSD=X": ("EUR/USD", 0.0001), "GBPUSD=X": ("GBP/USD", 0.0001),
    "USDJPY=X": ("USD/JPY", 0.01), "USDCHF=X": ("USD/CHF", 0.0001),
    "AUDUSD=X": ("AUD/USD", 0.0001), "USDCAD=X": ("USD/CAD", 0.0001),
    "NZDUSD=X": ("NZD/USD", 0.0001),
}
FUTURES = {
    "ES=F": ("E-mini S&P 500", 0.25, 50), "NQ=F": ("E-mini Nasdaq-100", 0.25, 20),
    "YM=F": ("E-mini Dow", 1.0, 5), "RTY=F": ("E-mini Russell 2000", 0.1, 50),
    "CL=F": ("WTI crude oil", 0.01, 1000), "GC=F": ("Gold", 0.1, 100),
    "SI=F": ("Silver", 0.005, 5000), "HG=F": ("Copper", 0.0005, 25000),
    "NG=F": ("Natural gas", 0.001, 10000), "ZC=F": ("Corn", 0.25, 50),
    "ZS=F": ("Soybeans", 0.25, 50), "ZW=F": ("Wheat", 0.25, 50),
}
STRATS = [
    ("Donchian20_10_TP3R", 3.0), ("MACD12_26_9_TP2R", 2.0),
    ("RSI14_EMA200_TP2R", 2.0), ("EMA50_200_TP3R", 3.0),
    ("Supertrend10_3_TP3R", 3.0), ("Bollinger20_2_TP2R", 2.0),
    ("RSI2_EMA200_TP2R", 2.0), ("Volume_Donchian20_TP3R", 3.0),
]


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 five-year-backtest"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())


def yahoo_daily(symbol: str) -> pd.DataFrame:
    path = CACHE / f"{symbol.replace('=', '_')}_1d.csv"
    if path.exists():
        d = pd.read_csv(path, parse_dates=["timestamp"]); d.timestamp = pd.to_datetime(d.timestamp, utc=True)
        return d
    p1 = int(WARM.timestamp()); p2 = int(END.timestamp())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol, safe='')}?period1={p1}&period2={p2}&interval=1d&events=history"
    data = get_json(url)["chart"]; result = data["result"]
    if not result: raise RuntimeError(f"Yahoo {symbol}: {data.get('error')}")
    r = result[0]; q = r["indicators"]["quote"][0]
    d = pd.DataFrame({"timestamp":pd.to_datetime(r["timestamp"], unit="s", utc=True), **{k:q[k] for k in ["open","high","low","close","volume"]}})
    d = d.dropna(subset=["open","high","low","close"]).reset_index(drop=True)
    d.to_csv(path,index=False); time.sleep(.15); return d


def binance_daily(symbol: str) -> pd.DataFrame:
    path = CACHE / f"{symbol}_UM_1d.csv"
    if path.exists():
        d=pd.read_csv(path,parse_dates=["timestamp"]); d.timestamp=pd.to_datetime(d.timestamp,utc=True)
        if d.timestamp.max() >= END-pd.Timedelta(days=1): return d
        current=[]
        for day in pd.date_range(d.timestamp.max().normalize()+pd.Timedelta(days=1), pd.Timestamp("2026-10-09",tz="UTC"), freq="D"):
            ds=day.strftime("%Y-%m-%d"); url=f"https://data.binance.vision/data/futures/um/daily/klines/{symbol}/1d/{symbol}-1d-{ds}.zip"
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 five-year-backtest"})
                with urllib.request.urlopen(req,timeout=30) as resp: payload=resp.read()
                z=zipfile.ZipFile(io.BytesIO(payload)); a=pd.read_csv(z.open(z.namelist()[0]),header=None)
                if str(a.iloc[0,0])=="open_time": a=a.iloc[1:]
                a=a.iloc[:,:6]; a.columns=["open_ms","open","high","low","close","volume"]
                a["timestamp"]=pd.to_datetime(pd.to_numeric(a.open_ms),unit="ms",utc=True)
                current.append(a[["timestamp","open","high","low","close","volume"]])
            except Exception as e:
                if getattr(e,"code",None) not in (404,): print("warning",symbol,ds,str(e)[:120],flush=True)
        if current:
            d=pd.concat([d,*current],ignore_index=True).drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True); d.to_csv(path,index=False)
        return d
    months = pd.period_range("2021-07", "2026-09", freq="M"); parts=[]
    for m in months:
        ym=str(m); url=f"https://data.binance.vision/data/futures/um/monthly/klines/{symbol}/1d/{symbol}-1d-{ym}.zip"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 five-year-backtest"})
            with urllib.request.urlopen(req,timeout=45) as resp: payload=resp.read()
            z=zipfile.ZipFile(io.BytesIO(payload)); a=pd.read_csv(z.open(z.namelist()[0]),header=None)
            if str(a.iloc[0,0])=="open_time": a=a.iloc[1:]
            a=a.iloc[:,:6]; a.columns=["open_ms","open","high","low","close","volume"]
            a["timestamp"]=pd.to_datetime(pd.to_numeric(a.open_ms),unit="ms",utc=True)
            parts.append(a[["timestamp","open","high","low","close","volume"]])
        except Exception as e:
            # Some symbols were listed after the start date; absent month files are expected.
            if getattr(e,"code",None) not in (404,): print("warning",symbol,ym,str(e)[:120],flush=True)
        time.sleep(.015)
    for day in pd.date_range(pd.Timestamp("2026-10-01",tz="UTC"), pd.Timestamp("2026-10-09",tz="UTC"), freq="D"):
        ds=day.strftime("%Y-%m-%d")
        url=f"https://data.binance.vision/data/futures/um/daily/klines/{symbol}/1d/{symbol}-1d-{ds}.zip"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 five-year-backtest"})
            with urllib.request.urlopen(req,timeout=30) as resp: payload=resp.read()
            z=zipfile.ZipFile(io.BytesIO(payload)); a=pd.read_csv(z.open(z.namelist()[0]),header=None)
            if str(a.iloc[0,0])=="open_time": a=a.iloc[1:]
            a=a.iloc[:,:6]; a.columns=["open_ms","open","high","low","close","volume"]
            a["timestamp"]=pd.to_datetime(pd.to_numeric(a.open_ms),unit="ms",utc=True)
            parts.append(a[["timestamp","open","high","low","close","volume"]])
        except Exception as e:
            if getattr(e,"code",None) not in (404,): print("warning",symbol,ds,str(e)[:120],flush=True)
    if not parts: raise RuntimeError(f"No Binance UM daily data for {symbol}")
    d=pd.concat(parts,ignore_index=True)
    d[['open','high','low','close','volume']] = d[['open','high','low','close','volume']].astype(float)
    d=d.drop_duplicates("timestamp").sort_values("timestamp")
    d=d[(d.timestamp>=WARM)&(d.timestamp<END)].reset_index(drop=True); d.to_csv(path,index=False); return d


def rsi(c: pd.Series, n: int) -> pd.Series:
    delta=c.diff(); g=delta.clip(lower=0).ewm(alpha=1/n,adjust=False,min_periods=n).mean(); l=(-delta.clip(upper=0)).ewm(alpha=1/n,adjust=False,min_periods=n).mean()
    v=100-100/(1+g/l.replace(0,np.nan)); return v.where(l!=0,np.where(g==0,50.,100.))


def indicators(d: pd.DataFrame) -> pd.DataFrame:
    d=d.copy(); c=d.close; prev=c.shift(1)
    tr=pd.concat([d.high-d.low,(d.high-prev).abs(),(d.low-prev).abs()],axis=1).max(axis=1)
    d["atr"]=tr.ewm(alpha=1/14,adjust=False,min_periods=14).mean(); d["atr10"]=tr.ewm(alpha=.1,adjust=False,min_periods=10).mean()
    d["ema50"]=c.ewm(span=50,adjust=False).mean(); d["ema200"]=c.ewm(span=200,adjust=False).mean()
    d["hi20"]=d.high.shift(1).rolling(20,min_periods=20).max(); d["lo20"]=d.low.shift(1).rolling(20,min_periods=20).min()
    d["hi10"]=d.high.shift(1).rolling(10,min_periods=10).max(); d["lo10"]=d.low.shift(1).rolling(10,min_periods=10).min()
    d["volsma20"]=d.volume.rolling(20,min_periods=20).mean()
    m=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean(); ms=m.ewm(span=9,adjust=False).mean(); d["macd"],d["macdsig"]=m,ms
    d["rsi14"],d["rsi2"]=rsi(c,14),rsi(c,2)
    d["bbmid"]=c.rolling(20,min_periods=20).mean(); sd=c.rolling(20,min_periods=20).std(ddof=0); d["bblow"],d["bbhi"]=d.bbmid-2*sd,d.bbmid+2*sd
    mid=(d.high+d.low)/2; bu=mid+3*d.atr10; bl=mid-3*d.atr10; fu=np.full(len(d),np.nan); fl=np.full(len(d),np.nan); direction=np.zeros(len(d),dtype=np.int8)
    for i in range(len(d)):
        if not np.isfinite(d.atr10.iat[i]): continue
        if i==0 or not np.isfinite(fu[i-1]): fu[i],fl[i],direction[i]=bu.iat[i],bl.iat[i],1; continue
        fu[i]=bu.iat[i] if (bu.iat[i]<fu[i-1] or c.iat[i-1]>fu[i-1]) else fu[i-1]
        fl[i]=bl.iat[i] if (bl.iat[i]>fl[i-1] or c.iat[i-1]<fl[i-1]) else fl[i-1]
        direction[i]=1 if (direction[i-1]<0 and c.iat[i]>fu[i]) else -1 if (direction[i-1]>0 and c.iat[i]<fl[i]) else direction[i-1]
    d["st_dir"]=direction
    return d


def make_signals(d: pd.DataFrame, strategy: str) -> np.ndarray:
    n=len(d); s=np.zeros(n,dtype=np.int8); c=d.close.to_numpy(); p=np.r_[c[0],c[:-1]]
    names=[x[0] for x in STRATS]; ix=names.index(strategy)
    # Signals are positions in {-1,0,+1}, calculated at completed daily close.
    state=0
    for i in range(n):
        row=d.iloc[i]; prev=d.iloc[i-1] if i else row; nxt=state
        if ix in (0,7):
            volok=ix==0 or (pd.notna(row.volsma20) and row.volume>1.5*row.volsma20)
            if pd.notna(row.hi20) and c[i]>row.hi20 and volok: nxt=1
            elif pd.notna(row.lo20) and c[i]<row.lo20 and volok: nxt=-1
            elif state==1 and pd.notna(row.lo10) and c[i]<row.lo10: nxt=0
            elif state==-1 and pd.notna(row.hi10) and c[i]>row.hi10: nxt=0
        elif ix==1:
            if row.macd>row.macdsig and prev.macd<=prev.macdsig: nxt=1
            elif row.macd<row.macdsig and prev.macd>=prev.macdsig: nxt=-1
        elif ix==2:
            if c[i]>row.ema200 and prev.rsi14<=30<row.rsi14: nxt=1
            elif c[i]<row.ema200 and prev.rsi14>=70>row.rsi14: nxt=-1
            elif state==1 and (c[i]<row.ema200 or row.rsi14>=60): nxt=0
            elif state==-1 and (c[i]>row.ema200 or row.rsi14<=40): nxt=0
        elif ix==3:
            if row.ema50>row.ema200 and prev.ema50<=prev.ema200: nxt=1
            elif row.ema50<row.ema200 and prev.ema50>=prev.ema200: nxt=-1
        elif ix==4:
            if row.st_dir>0 and prev.st_dir<=0: nxt=1
            elif row.st_dir<0 and prev.st_dir>=0: nxt=-1
        elif ix==5:
            if pd.notna(prev.bblow) and prev.close<=prev.bblow and c[i]>row.bblow: nxt=1
            elif pd.notna(prev.bbhi) and prev.close>=prev.bbhi and c[i]<row.bbhi: nxt=-1
            elif state==1 and c[i]>=row.bbmid: nxt=0
            elif state==-1 and c[i]<=row.bbmid: nxt=0
        elif ix==6:
            if c[i]>row.ema200 and row.rsi2<10: nxt=1
            elif c[i]<row.ema200 and row.rsi2>90: nxt=-1
            elif state==1 and (c[i]<row.ema200 or row.rsi2>70): nxt=0
            elif state==-1 and (c[i]>row.ema200 or row.rsi2<30): nxt=0
        s[i]=nxt; state=nxt
    return s


def costs(market: str, symbol: str) -> tuple[float,float]:
    """Return per-side price slippage+spread and fee fraction (or price units for futures)."""
    if market=="Crypto futures": return 0.0005,0.0005  # 5 bps slippage + 5 bps taker fee per side
    if market=="FX":
        pip=FX[symbol][1]; return pip*0.4,0.0 # 0.2 pip half-spread + 0.2 pip slippage each side
    tick,mult=FUTURES[symbol][1:]
    # One tick per side slippage and $2.50 commission/contract/side converted to price points.
    return tick+2.5/mult,0.0


def market_backtest(raw: pd.DataFrame, market: str, symbol: str, label: str, strategy: str, tp_r: float):
    d=indicators(raw)
    sig=make_signals(d,strategy)
    slip, fee=costs(market,symbol)
    closes=d.close.to_numpy(); opens=d.open.to_numpy(); highs=d.high.to_numpy(); lows=d.low.to_numpy(); atr=d.atr.to_numpy(); ts=d.timestamp
    trades=[]; side=0; entry=stop=take=0.; entry_i=0
    def adverse_slip(px: float) -> float:
        return slip*abs(px) if market=="Crypto futures" else slip
    for i in range(1,len(d)):
        if ts.iloc[i]<START: continue
        target=int(sig[i-1])
        # exit/stop before considering a new position. Position direction is stored in side.
        if side and target!=side:
            exit_price=opens[i]-side*adverse_slip(opens[i]); reason="訊號出場"
            risk=abs(entry-stop); pnl=side*(exit_price-entry)-fee*(abs(entry)+abs(exit_price))
            trades.append({"entry_time":ts.iloc[entry_i],"exit_time":ts.iloc[i],"side":side,"R":pnl/risk if risk else 0.,"reason":reason})
            side=0
        elif side:
            exit_price=None; reason=None
            if side==1:
                if opens[i]<=stop or lows[i]<=stop:
                    base=min(opens[i],stop); exit_price=base-adverse_slip(base); reason="止損"
                elif opens[i]>=take or highs[i]>=take:
                    exit_price=take-adverse_slip(take); reason="止盈"
                raw_pnl=side*(exit_price-entry) if exit_price is not None else None
            else:
                if opens[i]>=stop or highs[i]>=stop:
                    base=max(opens[i],stop); exit_price=base+adverse_slip(base); reason="止損"
                elif opens[i]<=take or lows[i]<=take:
                    exit_price=take+adverse_slip(take); reason="止盈"
                raw_pnl=side*(exit_price-entry) if exit_price is not None else None
            if exit_price is not None:
                risk=abs(entry-stop)
                # Two-side fees approximated as fraction of entry/exit notional.
                pnl=raw_pnl-fee*(abs(entry)+abs(exit_price))
                trades.append({"entry_time":ts.iloc[entry_i],"exit_time":ts.iloc[i],"side":side,"R":pnl/risk if risk else 0.,"reason":reason})
                side=0
        start_transition=(ts.iloc[i]>=START and ts.iloc[i-1]<START)
        if not side and target and (i==1 or sig[i-2]==0 or target!=int(sig[i-2]) or start_transition) and np.isfinite(atr[i-1]) and atr[i-1]>0:
            side=target; entry_i=i; entry=opens[i]+side*adverse_slip(opens[i])
            dist=1.5*atr[i-1]; stop=entry-side*dist; take=entry+side*tp_r*dist
            # If same bar hits both SL and TP, conservatively realize SL.
            slhit=(lows[i]<=stop if side==1 else highs[i]>=stop); tphit=(highs[i]>=take if side==1 else lows[i]<=take)
            if slhit:
                base=min(opens[i],stop) if side==1 else max(opens[i],stop); ex=base-side*adverse_slip(base); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex)); trades.append({"entry_time":ts.iloc[i],"exit_time":ts.iloc[i],"side":side,"R":pnl/dist,"reason":"止損"}); side=0
            elif tphit:
                ex=take-side*adverse_slip(take); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex)); trades.append({"entry_time":ts.iloc[i],"exit_time":ts.iloc[i],"side":side,"R":pnl/dist,"reason":"止盈"}); side=0
    if side:
        ex=closes[-1]-side*adverse_slip(closes[-1]); risk=abs(entry-stop); pnl=side*(ex-entry)-fee*(abs(entry)+abs(ex)); trades.append({"entry_time":ts.iloc[entry_i],"exit_time":ts.iloc[-1],"side":side,"R":pnl/risk if risk else 0.,"reason":"期末平倉"})
    return trades


def fixed_risk_stats(trades:list[dict], fraction:float):
    if not trades or not math.isfinite(fraction) or fraction<=0: return 0.,0.,0,False
    stake=INITIAL*fraction; equity=INITIAL; peak=equity; dd=0.; n=0; halted=False
    for t in trades:
        if equity<stake: halted=True; break
        equity+=float(t["R"])*stake; n+=1; peak=max(peak,equity); dd=max(dd,(peak-equity)/peak if peak else 0.)
        if equity<=0: equity=0; halted=True; break
    return (equity/INITIAL-1)*100,dd*100,n,halted


def formula_stats(trades:list[dict]):
    Rs=[float(t["R"]) for t in trades]; wins=[r for r in Rs if r>0]; losses=[-r for r in Rs if r<=0]
    if not Rs: return {"n":0,"p":float("nan"),"ev":float("nan"),"kelly":float("nan"),"wins":0}
    p=len(wins)/len(Rs); q=1-p; aw=float(np.mean(wins)) if wins else float("nan"); al=float(np.mean(losses)) if losses else float("nan")
    b=aw/al if wins and losses and al else float("nan"); k=(b*p-q)/b if math.isfinite(b) and b>0 else float("nan")
    return {"n":len(Rs),"p":p,"ev":float(np.mean(Rs)),"kelly":k,"wins":len(wins)}


def main():
    instruments=[]
    for s in CRYPTO: instruments.append(("Crypto futures",s,s,lambda s=s:binance_daily(s)))
    for s,(name,_) in FX.items(): instruments.append(("FX",s,name,lambda s=s:yahoo_daily(s)))
    for s,(name,_,_) in FUTURES.items(): instruments.append(("Traditional futures",s,name,lambda s=s:yahoo_daily(s)))
    results=[]; ledger=[]
    for market,symbol,label,loader in instruments:
        try:
            raw=loader(); raw=raw.dropna(subset=["open","high","low","close"]).sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
            for c in ["open","high","low","close","volume"]:
                if c in raw: raw[c]=pd.to_numeric(raw[c],errors="coerce")
            raw=raw.dropna(subset=["open","high","low","close"]).reset_index(drop=True)
            raw=raw[(raw.timestamp>=WARM)&(raw.timestamp<END)].reset_index(drop=True)
            if len(raw)<250: print("skip short",symbol,len(raw)); continue
            actual_start=str(raw.loc[raw.timestamp>=START,"timestamp"].min())
            print("DATA",market,label,len(raw),actual_start,str(raw.timestamp.max()),flush=True)
            for strategy,tp in STRATS:
                trs=market_backtest(raw,market,symbol,label,strategy,tp); Rs=[float(t["R"]) for t in trs]
                w=[r for r in Rs if r>0]; l=[-r for r in Rs if r<=0]; p=len(w)/len(Rs) if Rs else float("nan"); q=1-p if Rs else float("nan")
                aw=np.mean(w) if w else float("nan"); al=np.mean(l) if l else float("nan"); b=aw/al if w and l and al else float("nan")
                k=(b*p-q)/b if math.isfinite(b) and b>0 else float("nan")
                maxloss=cur=0
                for r in Rs: cur=cur+1 if r<=0 else 0; maxloss=max(maxloss,cur)
                counts={why:sum(t["reason"]==why for t in trs) for why in ["止盈","止損","訊號出場","期末平倉"]}
                is_trades=[t for t in trs if pd.Timestamp(t["entry_time"])<OOS]; oos_trades=[t for t in trs if pd.Timestamp(t["entry_time"])>=OOS]
                isfm=formula_stats(is_trades); oosfm=formula_stats(oos_trades); kis=isfm["kelly"]
                methods=[("固定1R",FIXED_RISK,FIXED_RISK),("全凱利",max(0,k) if math.isfinite(k) else 0,max(0,kis) if math.isfinite(kis) else 0),
                         ("半凱利",max(0,k/2) if math.isfinite(k) else 0,max(0,kis/2) if math.isfinite(kis) else 0),
                         ("四分之一凱利",max(0,k/4) if math.isfinite(k) else 0,max(0,kis/4) if math.isfinite(kis) else 0)]
                for method,f,isf in methods:
                    ret,dd,done,halted=fixed_risk_stats(trs,f)
                    oosret,oosdd,oosdone,ooshalted=fixed_risk_stats(oos_trades,isf)
                    results.append({"倉位方法":method,"市場":market,"商品":label,"代碼":symbol,"週期":"1d","策略":strategy,"TP_R":tp,"資料起始":actual_start,"K線數":len(raw),"交易數":len(trs),"止盈數":counts["止盈"],"止損數":counts["止損"],"訊號出場數":counts["訊號出場"],"期末平倉數":counts["期末平倉"],"勝率":p,"平均獲利R":aw,"平均虧損R":al,"盈虧比b":b,"EV_R每筆":float(np.mean(Rs)) if Rs else float("nan"),"IS_交易數":isfm["n"],"IS_勝率":isfm["p"],"IS_EV_R":isfm["ev"],"IS_凱利比例":kis,"OOS_交易數":oosfm["n"],"OOS_勝率":oosfm["p"],"OOS_EV_R":oosfm["ev"],"OOS_起始風險比例_僅以IS估計":isf,"OOS_收益_pct":oosret,"OOS_最大回撤_pct":oosdd,"OOS_資金不足停止":ooshalted,"原始全凱利比例":k,"實際固定風險比例":f,"五年收益_pct":ret,"最大回撤_pct":dd,"最大連敗":maxloss,"q連敗次方":q**maxloss if maxloss and math.isfinite(q) else float("nan"),"已完成交易數":done,"資金不足停止":halted})
                for j,t in enumerate(trs,1): ledger.append({"市場":market,"商品":label,"代碼":symbol,"策略":strategy,"trade_no":j,**t})
        except Exception as e:
            print("ERROR",market,symbol,type(e).__name__,str(e)[:250],flush=True)
    x=pd.DataFrame(results)
    if x.empty: raise RuntimeError("No backtests completed")
    x=x.sort_values("五年收益_pct",ascending=False).reset_index(drop=True); x.insert(0,"綜合排名",np.arange(1,len(x)+1))
    x.to_csv(ROOT/"five_year_all_kelly_ranked.csv",index=False)
    pd.DataFrame(ledger).to_csv(ROOT/"five_year_all_market_trade_ledger.csv",index=False)
    top=x.head(20)
    lines=["# 五年多市場策略 × 凱利方式綜合排名","",f"回測期間：{START.date()} 至 {END.date()} UTC；日線；資料暖機自 {WARM.date()}。前四年 IS，最後一年 OOS（{OOS.date()} 至 {END.date()}）。成功跑完 {x['代碼'].nunique()} 個商品、{x.groupby(['市場','商品','策略']).ngroups} 個市場×商品×策略組合，四種倉位方式各列一列，共 {len(x)} 列。","","## 前 20 名（將四種凱利方式視為獨立策略）","","|#|倉位|市場|商品|週期|策略|五年筆數|TP/SL|勝率|EV (R)|風險比例|五年收益|五年最大回撤|IS估凱利的OOS收益|OOS筆數|","|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in top.itertuples(index=False): lines.append(f"|{r.綜合排名}|{r.倉位方法}|{r.市場}|{r.商品}|{r.週期}|{r.策略}|{r.交易數}|{r.止盈數}/{r.止損數}|{r.勝率:.1%}|{r.EV_R每筆:.3f}|{r.實際固定風險比例:.2%}|{r.五年收益_pct:.2f}%|{r.最大回撤_pct:.2f}%|{r.OOS_收益_pct:.2f}%|{r.OOS_交易數}|")
    lines += ["","## 方法與限制","","- 每筆以已完成交易的淨損益除以初始止損距離計 R；`p=勝率`、`q=1-p`、`b=平均獲利R/平均虧損R`、`EV=p×平均獲利R−q×平均虧損R`、`f*=(bp−q)/b`。半凱利= f*/2，四分之一凱利=f*/4；負凱利以不交易 (0%) 處理。","- 固定初始本金 $10,000。為延續前次講義 1R 的算法，固定 1R 取初始本金 10%；凱利各比例依初始本金固定美元風險、不複利，餘額不足以承擔下一筆固定風險時停止。","- 策略使用收盤訊號、下一根開盤進場；ATR(14) 1.5 倍止損，策略表列固定 2R 或 3R 止盈；K 線同時碰 SL/TP 時 SL 優先。市場成本：Binance UM 假設單邊 5bps 手續費+5bps 滑價，FX 假設每邊 0.4 pip 成本，傳統期貨連續合約假設每邊 1 tick 滑價+$2.50/口佣金。","- 外匯與傳統期貨用 Yahoo Finance 日線；期貨代碼為連續合約（例如 ES=F、CL=F），換月與 back-adjustment 細節不可視為交易所逐合約成交資料。Binance 為 USD-M 永續日線；未計 funding、強平與保證金規則。未計稅。成本設定是研究假設，不是每家券商/交易所的實際費率。Yahoo 將金融行情明示為資訊用途、非交易用途。","- 同一報告中的 FX/期貨/加密貨幣都用日線比較；各資料源、交易時段、合約規格與可交易歷史仍不同。五年收益與最大回撤使用樣本全段估計的 Kelly，屬樣本內排名；OOS 欄位使用前四年 IS 估計的倉位比例，另測最後一年，但不是滾動 walk-forward。最大回撤以逐筆平倉權益計算，未 mark-to-market 持倉內浮動回撤。","- 輸出 CSV 收錄所有完成組合的四種倉位排名、IS/OOS 和各筆交易數；逐筆交易明細收錄每筆 R 和出場原因。資料缺漏或下載失敗的商品會在執行輸出標記 ERROR，不得當作零收益。"]
    (ROOT/"five_year_all_kelly_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("TOP20\n",top[["綜合排名","倉位方法","市場","商品","策略","交易數","五年收益_pct","最大回撤_pct"]].to_string(index=False)); print("saved",len(x),"rows",flush=True)

if __name__=="__main__": main()
