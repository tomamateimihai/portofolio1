"""
S&P 500 Stock Market Analysis - Exploratory Data Analysis (EDA)
===============================================================
This script performs comprehensive EDA on S&P 500 stock data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Define analysis parameters
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365)  # Last 1 year of data

# Top S&P 500 companies (updated tickers)
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'UNH', 'JNJ',
    'V', 'XOM', 'JPM', 'PG', 'MA', 'HD', 'CVX', 'LLY', 'ABBV', 'MRK',
    'PEP', 'KO', 'COST', 'AVGO', 'TMO', 'WMT', 'MCD', 'CSCO', 'ACN', 'DIS',
    'ABT', 'DHR', 'CRM', 'WFC', 'NEE', 'TXN', 'NKE', 'PM', 'UNP', 'BA',
    'HON', 'LOW', 'INTC', 'UPS', 'IBM', 'CAT', 'SBUX', 'AMD', 'GE', 'INTU'
]

print("=" * 70)
print("S&P 500 STOCK MARKET ANALYSIS - EXPLORATORY DATA ANALYSIS")
print("=" * 70)
print(f"\nAnalysis Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
print(f"Number of Stocks: {len(TICKERS)}")

# ============================================================
# STEP 1: Download Stock Data
# ============================================================
print("\n" + "=" * 70)
print("STEP 1: DOWNLOADING STOCK DATA")
print("=" * 70)

# Download all data at once with multi-ticker download
print("Downloading stock data from Yahoo Finance...")
try:
    stock_data = yf.download(TICKERS, start=START_DATE, end=END_DATE, progress=True)
    print(f"\nData downloaded successfully!")
    print(f"Shape: {stock_data.shape}")
    print(f"Columns: {stock_data.columns.tolist()[:10]}...")
except Exception as e:
    print(f"Error downloading data: {e}")
    raise

# Handle multi-level columns if present
if isinstance(stock_data.columns, pd.MultiIndex):
    print("Detected multi-level columns, extracting price data...")
    adj_close = stock_data['Adj Close'] if 'Adj Close' in stock_data.columns.get_level_values(0) else stock_data['Close']
    close = stock_data['Close']
    volume = stock_data['Volume']
    high = stock_data['High']
    low = stock_data['Low']
    open_price = stock_data['Open']
else:
    adj_close = stock_data['Adj Close'] if 'Adj Close' in stock_data.columns else stock_data['Close']
    close = stock_data['Close']
    volume = stock_data['Volume']
    high = stock_data['High']
    low = stock_data['Low']
    open_price = stock_data['Open']

# ============================================================
# STEP 2: Data Cleaning and Preprocessing
# ============================================================
print("\n" + "=" * 70)
print("STEP 2: DATA CLEANING AND PREPROCESSING")
print("=" * 70)

print(f"\nAdjusted Close Prices Shape: {adj_close.shape}")
print(f"Date Range: {adj_close.index.min()} to {adj_close.index.max()}")

# Check for missing values
print("\n--- Missing Values Analysis ---")
missing_pct = (adj_close.isnull().sum() / len(adj_close) * 100).sort_values(ascending=False)
stocks_with_missing = missing_pct[missing_pct > 0]
if len(stocks_with_missing) > 0:
    print("\nStocks with missing data (%):")
    print(stocks_with_missing.head(10))
else:
    print("No missing data in adjusted close prices!")

# Fill missing values using forward fill then backward fill
adj_close_filled = adj_close.fillna(method='ffill').fillna(method='bfill')
volume_filled = volume.fillna(0)

print(f"\n--- Data Quality Summary ---")
print(f"Total trading days: {len(adj_close_filled)}")
print(f"Number of stocks: {len(adj_close_filled.columns)}")
print(f"Missing values after cleaning: {adj_close_filled.isnull().sum().sum()}")

# Remove stocks with all NaN
valid_columns = adj_close_filled.columns[adj_close_filled.notna().any()]
adj_close_filled = adj_close_filled[valid_columns]
volume_filled = volume_filled[valid_columns]

print(f"Valid stocks for analysis: {len(adj_close_filled.columns)}")

# ============================================================
# STEP 3: Calculate Returns and Performance Metrics
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: CALCULATING RETURNS AND PERFORMANCE METRICS")
print("=" * 70)

# Daily returns
daily_returns = adj_close_filled.pct_change().dropna()

# Calculate key metrics
metrics = pd.DataFrame(index=adj_close_filled.columns)

# Total Return
metrics['Total Return (%)'] = ((adj_close_filled.iloc[-1] / adj_close_filled.iloc[0]) - 1) * 100

# Annualized Return (assuming 252 trading days)
days = len(adj_close_filled)
metrics['Annualized Return (%)'] = ((1 + metrics['Total Return (%)']/100) ** (252/days) - 1) * 100

# Volatility (Annualized Standard Deviation)
metrics['Volatility (%)'] = daily_returns.std() * np.sqrt(252) * 100

# Sharpe Ratio (assuming risk-free rate of 4%)
risk_free_rate = 0.04
metrics['Sharpe Ratio'] = (metrics['Annualized Return (%)']/100 - risk_free_rate) / (metrics['Volatility (%)']/100)

# Maximum Drawdown
def max_drawdown(prices):
    peak = prices.cummax()
    drawdown = (prices - peak) / peak
    return drawdown.min() * 100

metrics['Max Drawdown (%)'] = adj_close_filled.apply(max_drawdown)

# Average Volume
metrics['Avg Volume (M)'] = volume_filled.mean() / 1e6

# Current Price
metrics['Current Price ($)'] = adj_close_filled.iloc[-1]

# 50-day and 200-day Moving Averages
ma50 = adj_close_filled.rolling(window=50).mean()
ma200 = adj_close_filled.rolling(window=200).mean()
metrics['MA50 ($)'] = ma50.iloc[-1]
metrics['MA200 ($)'] = ma200.iloc[-1]

# Price above/below moving averages
metrics['Above MA50'] = (adj_close_filled.iloc[-1] > ma50.iloc[-1]).astype(int)
metrics['Above MA200'] = (adj_close_filled.iloc[-1] > ma200.iloc[-1]).astype(int)

# Sort by total return
metrics_sorted = metrics.sort_values('Total Return (%)', ascending=False)

print("\n--- Top 10 Performers ---")
print(metrics_sorted[['Total Return (%)', 'Annualized Return (%)', 'Volatility (%)', 'Sharpe Ratio']].head(10).to_string())

print("\n--- Bottom 10 Performers ---")
print(metrics_sorted[['Total Return (%)', 'Annualized Return (%)', 'Volatility (%)', 'Sharpe Ratio']].tail(10).to_string())

# ============================================================
# STEP 4: Exploratory Data Analysis - Visualizations
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: CREATING VISUALIZATIONS")
print("=" * 70)

# Create output directory for plots
import os
output_dir = 'sp500_analysis_plots'
os.makedirs(output_dir, exist_ok=True)

# Figure 1: Stock Price Trends (Line Chart)
print("\nCreating Figure 1: Stock Price Trends...")
fig1, axes = plt.subplots(2, 1, figsize=(14, 10))

# Normalized price chart (rebased to 100)
normalized_prices = adj_close_filled / adj_close_filled.iloc[0] * 100
top_10 = metrics_sorted.head(10).index.tolist()

ax1 = axes[0]
for ticker in top_10:
    ax1.plot(normalized_prices.index, normalized_prices[ticker], label=ticker, linewidth=1.5)
ax1.set_title('Top 10 Performers - Normalized Price Trends (Rebased to 100)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Normalized Price')
ax1.legend(loc='upper left', fontsize=8)
ax1.grid(True, alpha=0.3)

# Bottom 10 performers
bottom_10 = metrics_sorted.tail(10).index.tolist()
ax2 = axes[1]
for ticker in bottom_10:
    ax2.plot(normalized_prices.index, normalized_prices[ticker], label=ticker, linewidth=1.5)
ax2.set_title('Bottom 10 Performers - Normalized Price Trends (Rebased to 100)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Date')
ax2.set_ylabel('Normalized Price')
ax2.legend(loc='upper left', fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/01_price_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/01_price_trends.png")

# Figure 2: Return Distribution
print("Creating Figure 2: Return Distributions...")
fig2, axes = plt.subplots(1, 2, figsize=(14, 6))

# Histogram of daily returns
ax1 = axes[0]
returns_flat = daily_returns.values.flatten()
returns_flat = returns_flat[~np.isnan(returns_flat)]
ax1.hist(returns_flat, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax1.set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold')
ax1.set_xlabel('Daily Return')
ax1.set_ylabel('Frequency')
ax1.grid(True, alpha=0.3)

# Box plot of returns by stock
ax2 = axes[1]
top_15_tickers = metrics_sorted.head(15).index.tolist()
returns_for_box = daily_returns[top_15_tickers].copy()
returns_for_box.boxplot(ax=ax2, rot=90)
ax2.set_title('Daily Returns Distribution (Top 15 Performers)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Stock Ticker')
ax2.set_ylabel('Daily Return')
ax2.axhline(y=0, color='red', linestyle='--', linewidth=1)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/02_return_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/02_return_distributions.png")

# Figure 3: Risk-Return Analysis (Scatter Plot)
print("Creating Figure 3: Risk-Return Analysis...")
fig3, ax = plt.subplots(figsize=(12, 8))

# Scatter plot
scatter = ax.scatter(metrics['Volatility (%)'], 
                     metrics['Annualized Return (%)'],
                     s=metrics['Avg Volume (M)']*2,
                     c=metrics['Sharpe Ratio'],
                     cmap='RdYlGn',
                     alpha=0.7,
                     edgecolors='black',
                     linewidth=0.5)

# Add labels for top performers
for idx in metrics_sorted.head(10).index:
    ax.annotate(idx, 
                (metrics.loc[idx, 'Volatility (%)'], metrics.loc[idx, 'Annualized Return (%)']),
                fontsize=8,
                ha='center',
                va='bottom')

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax.set_xlabel('Volatility (Annualized %)', fontsize=12)
ax.set_ylabel('Annualized Return (%)', fontsize=12)
ax.set_title('Risk-Return Analysis (Size = Avg Volume, Color = Sharpe Ratio)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='Sharpe Ratio')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/03_risk_return.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/03_risk_return.png")

# Figure 4: Correlation Matrix
print("Creating Figure 4: Correlation Matrix...")
fig4, ax = plt.subplots(figsize=(14, 12))

# Calculate correlation matrix
corr_matrix = daily_returns.corr()

# Create heatmap
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, 
            mask=mask,
            annot=False,
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax)
ax.set_title('Stock Returns Correlation Matrix', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/04_correlation_matrix.png")

# Figure 5: Sector Performance Comparison (Bar Chart)
print("Creating Figure 5: Performance Bar Chart...")
fig5, ax = plt.subplots(figsize=(14, 8))

# Sort by total return
sorted_metrics = metrics.sort_values('Total Return (%)', ascending=True)
colors = ['green' if x > 0 else 'red' for x in sorted_metrics['Total Return (%)']]

ax.barh(sorted_metrics.index, sorted_metrics['Total Return (%)'], color=colors, alpha=0.7, edgecolor='black')
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
ax.set_xlabel('Total Return (%)', fontsize=12)
ax.set_ylabel('Stock Ticker', fontsize=12)
ax.set_title('Stock Performance - Total Return (%)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_performance_bar.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/05_performance_bar.png")

# Figure 6: Volatility Analysis
print("Creating Figure 6: Volatility Analysis...")
fig6, axes = plt.subplots(1, 2, figsize=(14, 6))

# Volatility distribution
ax1 = axes[0]
vol_data = metrics['Volatility (%)'].dropna()
ax1.hist(vol_data, bins=20, alpha=0.7, color='coral', edgecolor='black')
ax1.axvline(x=vol_data.mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {vol_data.mean():.1f}%")
ax1.set_xlabel('Volatility (Annualized %)', fontsize=12)
ax1.set_ylabel('Number of Stocks', fontsize=12)
ax1.set_title('Volatility Distribution', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Top volatile stocks
ax2 = axes[1]
vol_sorted = metrics.sort_values('Volatility (%)', ascending=False).head(15)
ax2.barh(vol_sorted.index, vol_sorted['Volatility (%)'], color='coral', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Volatility (Annualized %)', fontsize=12)
ax2.set_ylabel('Stock Ticker', fontsize=12)
ax2.set_title('Top 15 Most Volatile Stocks', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(f'{output_dir}/06_volatility_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/06_volatility_analysis.png")

# Figure 7: Moving Averages Analysis
print("Creating Figure 7: Moving Averages Analysis...")
fig7, ax = plt.subplots(figsize=(14, 8))

# Plot S&P 500 ETF (SPY) or average of stocks as market proxy
market_avg = adj_close_filled.mean(axis=1)
ma50_all = market_avg.rolling(window=50).mean()
ma200_all = market_avg.rolling(window=200).mean()

ax.plot(market_avg.index, market_avg, label='Market Average', linewidth=2, color='blue')
ax.plot(ma50_all.index, ma50_all, label='50-Day MA', linewidth=1.5, color='orange')
ax.plot(ma200_all.index, ma200_all, label='200-Day MA', linewidth=1.5, color='red')

ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Price ($)', fontsize=12)
ax.set_title('Market Average with Moving Averages', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/07_moving_averages.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/07_moving_averages.png")

# Figure 8: Volume Analysis
print("Creating Figure 8: Volume Analysis...")
fig8, axes = plt.subplots(1, 2, figsize=(14, 6))

# Volume over time (aggregate)
ax1 = axes[0]
total_volume = volume_filled.sum(axis=1)
ax1.bar(total_volume.index, total_volume/1e9, alpha=0.7, color='steelblue', width=1)
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Total Volume (Billions)', fontsize=12)
ax1.set_title('Total Trading Volume Over Time', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Average volume by stock
ax2 = axes[1]
vol_by_stock = metrics.sort_values('Avg Volume (M)', ascending=True).tail(20)
ax2.barh(vol_by_stock.index, vol_by_stock['Avg Volume (M)'], alpha=0.7, color='steelblue', edgecolor='black')
ax2.set_xlabel('Average Daily Volume (Millions)', fontsize=12)
ax2.set_ylabel('Stock Ticker', fontsize=12)
ax2.set_title('Top 20 Stocks by Average Volume', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(f'{output_dir}/08_volume_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir}/08_volume_analysis.png")

# ============================================================
# STEP 5: Statistical Summary
# ============================================================
print("\n" + "=" * 70)
print("STEP 5: STATISTICAL SUMMARY")
print("=" * 70)

print("\n--- Overall Market Statistics ---")
print(f"Average Return: {metrics['Annualized Return (%)'].mean():.2f}%")
print(f"Median Return: {metrics['Annualized Return (%)'].median():.2f}%")
print(f"Average Volatility: {metrics['Volatility (%)'].mean():.2f}%")
print(f"Average Sharpe Ratio: {metrics['Sharpe Ratio'].mean():.2f}")
print(f"Average Max Drawdown: {metrics['Max Drawdown (%)'].mean():.2f}%")

print("\n--- Best Performers (by Total Return) ---")
for i, (ticker, row) in enumerate(metrics_sorted.head(5).iterrows(), 1):
    print(f"{i}. {ticker}: {row['Total Return (%)']:.2f}% (Sharpe: {row['Sharpe Ratio']:.2f})")

print("\n--- Worst Performers (by Total Return) ---")
for i, (ticker, row) in enumerate(metrics_sorted.tail(5).iloc[::-1].iterrows(), 1):
    print(f"{i}. {ticker}: {row['Total Return (%)']:.2f}% (Sharpe: {row['Sharpe Ratio']:.2f})")

print("\n--- Risk Metrics ---")
print(f"Most Volatile: {metrics['Volatility (%)'].idxmax()} ({metrics['Volatility (%)'].max():.2f}%)")
print(f"Least Volatile: {metrics['Volatility (%)'].idxmin()} ({metrics['Volatility (%)'].min():.2f}%)")
print(f"Best Risk-Adjusted: {metrics['Sharpe Ratio'].idxmax()} (Sharpe: {metrics['Sharpe Ratio'].max():.2f})")
print(f"Worst Max Drawdown: {metrics['Max Drawdown (%)'].idxmin()} ({metrics['Max Drawdown (%)'].min():.2f}%)")

# Save metrics to CSV
metrics_sorted.to_csv('sp500_metrics.csv')
print(f"\nMetrics saved to: sp500_metrics.csv")

# Save correlation matrix to CSV
corr_matrix.to_csv('sp500_correlation.csv')
print(f"Correlation matrix saved to: sp500_correlation.csv")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print(f"\nTotal visualizations created: 8")
print(f"Output directory: {output_dir}/")
print(f"CSV files: sp500_metrics.csv, sp500_correlation.csv")
print("\n" + "=" * 70)
