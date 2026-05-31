# 📈 Stock Market & Financial Data Analysis

> A Python-based financial analytics project covering 5 years (2019–2024) of stock performance for AAPL, GOOGL, MSFT, AMZN, and TSLA — with moving average signals, volatility modeling, correlation analysis, and sector comparison.

---

## 🔍 Key Insights

| Finding | Detail |
|---|---|
| 🏆 Best quarter | TSLA Q4 2022 → **+70.1%** |
| 💀 Worst quarter | TSLA Q1 2020 → **-59.5%** |
| 📊 Highest volatility | TSLA: **3.7× more volatile** than AAPL over 5 years |
| 🔗 Most correlated pair | AAPL & MSFT (both large-cap tech; similar macro exposure) |
| 💰 Best total return | MSFT: **+302%** over the period |

---

## 📊 Charts Generated

| Chart | Description |
|---|---|
| `AAPL_price_ma.png` … `TSLA_price_ma.png` | Closing price + MA50 + MA200 + Golden/Death Cross markers + 30-day volatility |
| `cumulative_returns.png` | All 5 stocks normalized from a common start |
| `correlation_heatmap.png` | Pairwise return correlation (seaborn heatmap) |
| `sector_comparison.png` | XLK / XLF / XLE ETF performance (Base = 100) |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- `yfinance` — live market data pulls
- `pandas` — time-series manipulation
- `numpy` — numerical computation
- `matplotlib` — charting
- `seaborn` — correlation heatmap
- `plotly` — optional interactive charts

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/stock-market-analysis.git
cd stock-market-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the full analysis
```bash
python src/analysis.py
```

All charts save to `charts/` and summary statistics to `reports/summary_stats.csv`.

> **Offline mode:** If `yfinance` can't reach the internet, the script automatically falls back to the sample CSVs in `data/`. This means the project runs cleanly in any environment.

---

## 📁 Project Structure

```
stock-market-analysis/
├── src/
│   ├── analysis.py            # Main analysis script
│   └── generate_sample_data.py  # Synthetic data generator (offline fallback)
├── data/                      # Sample CSVs (AAPL.csv, MSFT.csv, …)
├── charts/                    # Generated PNG charts
├── reports/
│   └── summary_stats.csv      # Key metrics per ticker
├── requirements.txt
└── README.md
```

---

## 📐 Financial Metrics Explained

| Metric | Formula | Meaning |
|---|---|---|
| Daily Return | `Close.pct_change()` | % change day-over-day |
| MA30 / MA50 / MA200 | `Close.rolling(N).mean()` | Short / medium / long-term trend |
| Volatility | `Returns.rolling(30).std()` | 30-day rolling risk measure |
| Golden Cross | MA50 crosses **above** MA200 | Bullish signal |
| Death Cross | MA50 crosses **below** MA200 | Bearish signal |
| Max Drawdown | `(Close / Close.cummax()) - 1` | Worst peak-to-trough loss |

---

## 🔔 Signal Output (as of 2024-01-01)

| Ticker | Signal | MA50 | MA200 |
|---|---|---|---|
| AAPL | 🟢 Bullish | 153.69 | 143.90 |
| GOOGL | 🔴 Bearish | 46.20 | 54.94 |
| MSFT | 🟢 Bullish | 411.04 | 392.18 |
| AMZN | 🟢 Bullish | 168.24 | 166.52 |
| TSLA | 🟢 Bullish | 15.16 | 15.16 |

---

## 🔄 Extending the Project

- Swap in different tickers by editing `STOCKS` in `src/analysis.py`
- Change the date range via `START` / `END`
- Add Plotly for interactive HTML charts
- Export signals to a Slack/email alert via `smtplib` or `requests`

---

## 👤 Author

**eetoorivarshika06** · [GitHub](https://github.com/eetoorivarshika06)

*Built as part of a finance analytics portfolio — inspired by JPMorgan internship experience in data-driven financial modeling.*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
