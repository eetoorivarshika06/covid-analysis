"""
Stock Market & Financial Data Analysis
Author: Your Name
Description: 5-year analysis of AAPL/GOOGL/MSFT/AMZN/TSLA with moving averages,
             volatility, correlation, golden-cross signals, and sector comparison.
             Uses live yfinance data; falls back to sample CSVs if offline.
"""

import os, warnings
import pandas as pd
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

warnings.filterwarnings('ignore')

STOCKS  = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
SECTORS = {'XLK': 'Technology', 'XLF': 'Financials', 'XLE': 'Energy'}
START, END = '2019-01-01', '2024-01-01'

BASE     = os.path.dirname(os.path.abspath(__file__))
CHARTS   = os.path.join(BASE, '..', 'charts')
REPORTS  = os.path.join(BASE, '..', 'reports')
DATA_DIR = os.path.join(BASE, '..', 'data')
for d in (CHARTS, REPORTS): os.makedirs(d, exist_ok=True)

PALETTE = ['#2196F3','#4CAF50','#FF9800','#E91E63','#9C27B0']
plt.rcParams.update({
    'figure.facecolor':'#0D1117','axes.facecolor':'#161B22','axes.edgecolor':'#30363D',
    'text.color':'#E6EDF3','axes.labelcolor':'#E6EDF3','xtick.color':'#8B949E',
    'ytick.color':'#8B949E','grid.color':'#21262D','grid.linestyle':'--',
    'grid.linewidth':0.6,'legend.facecolor':'#161B22','legend.edgecolor':'#30363D',
    'font.family':'monospace',
})

def _load(ticker):
    csv = os.path.join(DATA_DIR, f'{ticker}.csv')
    try:
        import yfinance as yf
        df = yf.download(ticker, start=START, end=END, progress=False)
        df.columns = [c[0] if isinstance(c,tuple) else c for c in df.columns]
        if df.empty: raise ValueError
        print(f"   ✓  {ticker}: {len(df)} rows (live)")
        return df
    except Exception:
        df = pd.read_csv(csv, index_col=0, parse_dates=True)
        print(f"   ✓  {ticker}: {len(df)} rows (sample CSV)")
        return df

def compute_metrics(df):
    df = df.copy()
    df['Returns']    = df['Close'].pct_change()
    df['MA30']       = df['Close'].rolling(30).mean()
    df['MA50']       = df['Close'].rolling(50).mean()
    df['MA200']      = df['Close'].rolling(200).mean()
    df['Volatility'] = df['Returns'].rolling(30).std()
    df['CumReturn']  = (1 + df['Returns']).cumprod() - 1
    return df

def plot_price_ma(ticker, df):
    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(14,9),gridspec_kw={'height_ratios':[3,1]})
    fig.suptitle(f'{ticker} — Price & Moving Averages',fontsize=15,fontweight='bold',color='#E6EDF3',y=0.98)
    ax1.plot(df.index, df['Close'],  color='#58A6FF',lw=1.2, label='Close')
    ax1.plot(df.index, df['MA50'],   color='#F78166',lw=1.0, label='MA50',  ls='--')
    ax1.plot(df.index, df['MA200'],  color='#3FB950',lw=1.0, label='MA200', ls='--')
    gc = df[(df['MA50']>df['MA200'])&(df['MA50'].shift(1)<=df['MA200'].shift(1))].dropna()
    dc = df[(df['MA50']<df['MA200'])&(df['MA50'].shift(1)>=df['MA200'].shift(1))].dropna()
    if not gc.empty: ax1.scatter(gc.index,gc['Close'],marker='^',color='#3FB950',s=120,zorder=5,label='Golden Cross ▲')
    if not dc.empty: ax1.scatter(dc.index,dc['Close'],marker='v',color='#F78166',s=120,zorder=5,label='Death Cross ▼')
    ax1.set_ylabel('Price (USD)'); ax1.legend(loc='upper left',fontsize=8); ax1.grid(True)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.fill_between(df.index,df['Volatility'].fillna(0),color='#D29922',alpha=0.6,label='30d Volatility')
    ax2.set_ylabel('Volatility'); ax2.set_xlabel('Date'); ax2.legend(fontsize=8); ax2.grid(True)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    path = os.path.join(CHARTS,f'{ticker}_price_ma.png')
    plt.savefig(path,dpi=150,bbox_inches='tight'); plt.close(); print(f"   📊  {path}")

def plot_correlation(data):
    closes  = pd.DataFrame({t:d['Close'] for t,d in data.items()}).dropna()
    corr    = closes.pct_change().dropna().corr()
    fig,ax  = plt.subplots(figsize=(8,6))
    mask    = np.triu(np.ones_like(corr,dtype=bool))
    sns.heatmap(corr,annot=True,fmt='.2f',cmap='coolwarm',vmin=-1,vmax=1,ax=ax,mask=mask,
                linewidths=0.5,linecolor='#21262D',annot_kws={'size':11,'color':'#E6EDF3'})
    ax.set_title('Return Correlation Matrix',fontsize=13,fontweight='bold',color='#E6EDF3',pad=12)
    plt.tight_layout()
    path = os.path.join(CHARTS,'correlation_heatmap.png')
    plt.savefig(path,dpi=150,bbox_inches='tight'); plt.close(); print(f"   📊  {path}")

def plot_cumulative_returns(data):
    fig,ax = plt.subplots(figsize=(13,6))
    ax.set_title('Cumulative Returns (2019–2024)',fontsize=13,fontweight='bold',color='#E6EDF3',pad=12)
    for (ticker,df),color in zip(data.items(),PALETTE):
        ax.plot(df.index,df['CumReturn']*100,label=ticker,color=color,lw=1.5)
    ax.axhline(0,color='#8B949E',ls=':',lw=0.8)
    ax.set_ylabel('Cumulative Return (%)'); ax.set_xlabel('Date')
    ax.legend(fontsize=9); ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    path = os.path.join(CHARTS,'cumulative_returns.png')
    plt.savefig(path,dpi=150,bbox_inches='tight'); plt.close(); print(f"   📊  {path}")

def quarterly_performance(data):
    records = []
    for ticker,df in data.items():
        q = df['Close'].resample('QE').last().pct_change().dropna()
        for period,val in q.items():
            records.append({'Ticker':ticker,'Quarter':str(period.to_period('Q')),'Return':val})
    if not records: return
    qdf   = pd.DataFrame(records)
    best  = qdf.loc[qdf['Return'].idxmax()]
    worst = qdf.loc[qdf['Return'].idxmin()]
    print(f"\n🏆  Best  quarter : {best['Ticker']}  {best['Quarter']}  {best['Return']:+.1%}")
    print(f"💀  Worst quarter : {worst['Ticker']}  {worst['Quarter']}  {worst['Return']:+.1%}")

def generate_signals(data):
    print("\n🔔  Signal Report:")
    signals = []
    for ticker,df in data.items():
        valid = df.dropna(subset=['MA50','MA200'])
        if valid.empty: continue
        row    = valid.iloc[-1]
        signal = 'Bullish 🟢' if row['MA50']>row['MA200'] else 'Bearish 🔴'
        date   = row.name.date() if hasattr(row.name,'date') else row.name
        print(f"   {ticker}: {signal}  MA50={row['MA50']:.2f}  MA200={row['MA200']:.2f}  ({date})")
        signals.append({'Ticker':ticker,'Signal':signal,'Date':str(date),
                        'MA50':round(row['MA50'],2),'MA200':round(row['MA200'],2)})
    return signals

def plot_sector_comparison():
    print("\n📈  Sector ETFs …")
    fig,ax = plt.subplots(figsize=(13,6))
    ax.set_title('Sector ETF Normalized Performance (Base=100)',fontsize=13,fontweight='bold',color='#E6EDF3',pad=12)
    colors = ['#58A6FF','#3FB950','#F78166']
    for (etf,label),color in zip(SECTORS.items(),colors):
        df = _load(etf)
        norm = df['Close']/df['Close'].iloc[0]*100
        ax.plot(norm.index,norm,label=f'{etf} — {label}',color=color,lw=1.5)
        print(f"   ✓  {etf}")
    ax.axhline(100,color='#8B949E',ls=':',lw=0.8)
    ax.set_ylabel('Normalized Price (Base 100)'); ax.set_xlabel('Date')
    ax.legend(fontsize=9); ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    path = os.path.join(CHARTS,'sector_comparison.png')
    plt.savefig(path,dpi=150,bbox_inches='tight'); plt.close(); print(f"   📊  {path}")

def save_summary_stats(data, signals):
    rows = []
    for ticker,df in data.items():
        sig = next((s for s in signals if s['Ticker']==ticker),{})
        dd  = ((df['Close']/df['Close'].cummax())-1).min()
        rows.append({
            'Ticker':           ticker,
            'Start Price':      round(df['Close'].iloc[0],2),
            'End Price':        round(df['Close'].iloc[-1],2),
            'Total Return (%)': round(df['CumReturn'].dropna().iloc[-1]*100,2),
            'Avg Daily Ret (%)':round(df['Returns'].mean()*100,4),
            'Avg Volatility':   round(df['Volatility'].mean()*100,4),
            'Max Drawdown (%)': round(dd*100,2),
            'Signal':           sig.get('Signal','N/A'),
        })
    out  = pd.DataFrame(rows)
    path = os.path.join(REPORTS,'summary_stats.csv')
    out.to_csv(path,index=False)
    print(f"\n💾  Summary stats → {path}")
    print(out.to_string(index=False))

def main():
    print("="*60)
    print("  STOCK MARKET & FINANCIAL DATA ANALYSIS")
    print(f"  Period: {START} → {END}")
    print("="*60)
    print(f"\n📥  Loading data …")
    raw  = {t: _load(t) for t in STOCKS}
    data = {t: compute_metrics(df) for t,df in raw.items()}
    print("\n📊  Generating charts …")
    for ticker,df in data.items(): plot_price_ma(ticker,df)
    plot_correlation(data)
    plot_cumulative_returns(data)
    quarterly_performance(data)
    signals = generate_signals(data)
    plot_sector_comparison()
    save_summary_stats(data,signals)
    print("\n✅  Done!  charts/  and  reports/  are ready.")

if __name__ == '__main__':
    main()
