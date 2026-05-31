"""Generate realistic synthetic stock data for demo/portfolio purposes."""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

STOCKS = {
    'AAPL':  {'start': 39.5,  'mu': 0.00045, 'sigma': 0.016},
    'GOOGL': {'start': 61.0,  'mu': 0.00035, 'sigma': 0.017},
    'MSFT':  {'start': 101.0, 'mu': 0.00050, 'sigma': 0.015},
    'AMZN':  {'start': 83.0,  'mu': 0.00030, 'sigma': 0.019},
    'TSLA':  {'start': 23.0,  'mu': 0.00055, 'sigma': 0.038},
}
SECTORS = {
    'XLK': {'start': 65.0,  'mu': 0.00040, 'sigma': 0.014},
    'XLF': {'start': 27.0,  'mu': 0.00018, 'sigma': 0.012},
    'XLE': {'start': 60.0,  'mu': 0.00010, 'sigma': 0.017},
}

dates = pd.bdate_range('2019-01-01', '2024-01-01')

def simulate(start_price, mu, sigma, n):
    log_returns = np.random.normal(mu, sigma, n)
    prices = start_price * np.exp(np.cumsum(log_returns))
    prices = np.insert(prices, 0, start_price)[:n]
    return prices

def make_ohlcv(dates, prices):
    noise = np.random.uniform(0.995, 1.005, len(prices))
    df = pd.DataFrame({
        'Open':   prices * np.random.uniform(0.997, 1.003, len(prices)),
        'High':   prices * np.random.uniform(1.003, 1.012, len(prices)),
        'Low':    prices * np.random.uniform(0.988, 0.997, len(prices)),
        'Close':  prices,
        'Volume': np.random.randint(10_000_000, 80_000_000, len(prices)),
    }, index=dates)
    return df

out_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(out_dir, exist_ok=True)

all_data = {}
for ticker, p in {**STOCKS, **SECTORS}.items():
    prices = simulate(p['start'], p['mu'], p['sigma'], len(dates))
    df = make_ohlcv(dates, prices)
    df.to_csv(os.path.join(out_dir, f'{ticker}.csv'))
    all_data[ticker] = df
    print(f"✓ Generated {ticker}: {len(df)} rows, final price ${prices[-1]:.2f}")

print("\nAll sample data saved to data/")
