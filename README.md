# S&P 500 Stock Market Analysis - Exploratory Data Analysis (EDA)

## Project Overview

This project performs a comprehensive Exploratory Data Analysis (EDA) on 50 major S&P 500 companies, analyzing stock performance, risk metrics, and market trends over a 1-year period.

**Analysis Period:** March 2025 - February 2026  
**Stocks Analyzed:** 50 top S&P 500 companies  
**Data Source:** Yahoo Finance API (yfinance)

---

## Key Findings

### Top 5 Performers
| Rank | Stock | Total Return | Sharpe Ratio |
|------|-------|-------------|---------------|
| 1 | CAT (Caterpillar) | +126.80% | 3.72 |
| 2 | AMD | +103.82% | 1.57 |
| 3 | INTC (Intel) | +100.57% | 1.46 |
| 4 | GOOGL | +87.40% | 2.72 |
| 5 | AVGO | +72.09% | 1.39 |

### Bottom 5 Performers
| Rank | Stock | Total Return | Sharpe Ratio |
|------|-------|-------------|---------------|
| 1 | ACN (Accenture) | -38.90% | -1.29 |
| 2 | UNH (UnitedHealth) | -35.66% | -0.78 |
| 3 | CRM (Salesforce) | -33.10% | -1.07 |
| 4 | INTU | -31.49% | -1.03 |
| 5 | NKE (Nike) | -19.24% | -0.56 |

### Market Statistics
- **Average Return:** 18.78%
- **Median Return:** 12.12%
- **Average Volatility:** 31.94%
- **Average Sharpe Ratio:** 0.43
- **Most Volatile:** INTC (66.93%)
- **Least Volatile:** KO (16.93%)
- **Worst Max Drawdown:** UNH (-60.06%)

---

## Visualizations

1. **Price Trends** - Normalized performance of top/bottom 10 stocks
2. **Return Distributions** - Daily returns histogram and box plots
3. **Risk-Return Analysis** - Scatter plot (Volatility vs Return)
4. **Correlation Matrix** - Stock returns correlation heatmap
5. **Performance Bar Chart** - All stocks ranked by return
6. **Volatility Analysis** - Distribution and top volatile stocks
7. **Moving Averages** - Market trend with 50/200-day MAs
8. **Volume Analysis** - Trading volume patterns

---

## Technologies Used

- **Python 3.13** - Programming language
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **matplotlib** - Static visualization
- **seaborn** - Statistical visualization
- **yfinance** - Yahoo Finance data API

---

## How to Run

1. Install required libraries:
```bash
pip install yfinance pandas matplotlib seaborn numpy
```

2. Run the analysis:
```bash
python sp500_eda_analysis.py
```

3. View the generated visualizations in `sp500_analysis_plots/` folder

---

## Project Structure

```
datascientist/
├── README.md                    # This file
├── sp500_eda_analysis.py        # Main analysis script
├── sp500_metrics.csv            # Performance metrics data
├── sp500_correlation.csv        # Correlation matrix data
└── sp500_analysis_plots/        # Visualization outputs
    ├── 01_price_trends.png
    ├── 02_return_distributions.png
    ├── 03_risk_return.png
    ├── 04_correlation_matrix.png
    ├── 05_performance_bar.png
    ├── 06_volatility_analysis.png
    ├── 07_moving_averages.png
    └── 08_volume_analysis.png
```

---

## Skills Demonstrated

- **Data Acquisition:** Using yfinance API to fetch stock market data
- **Data Cleaning:** Handling missing values, forward/backward fill
- **Statistical Analysis:** Returns, volatility, Sharpe ratio, max drawdown
- **Data Visualization:** 8 professional chart types with matplotlib/seaborn
- **Financial Analysis:** Risk-adjusted returns, correlation analysis

---

## License

This project is for educational and portfolio demonstration purposes.

---

*Project completed: March 2026*
