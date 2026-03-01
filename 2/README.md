# 📈 S&P 500 Interactive Market Dashboard

A comprehensive interactive dashboard for S&P 500 stock analysis built with **Streamlit** and **Plotly**. This project demonstrates advanced data visualization, interactive UI design, and financial analysis capabilities.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-1.54.0-FF4B4B?style=flat&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)
![Plotly](https://img.shields.io/badge/Plotly-6.5.2-3F4F75?style=flat&logo=plotly)

## 🎯 Features

### 1. Stock Performance Trends
- **Interactive Bar Charts**: Visualize top performers by Total Return, Annualized Return, Volatility, or Sharpe Ratio
- **Summary Metrics**: Key performance indicators including average return, best/worst performers
- **Detailed Data Table**: Sortable and filterable performance metrics

### 2. Volatility Analysis
- **Risk-Return Scatter Plot**: Visualize the risk-return profile with Sharpe Ratio as bubble size
- **Volatility Distribution**: Histogram showing the distribution of volatility across stocks
- **High Volatility Identification**: Quick identification of the most volatile stocks

### 3. Correlation Heatmap
- **Interactive Correlation Matrix**: Color-coded heatmap showing stock correlations
- **Customizable Selection**: Multiselect to analyze specific stock subsets
- **Top Correlations**: Automatic display of strongest positive and negative correlations

### 4. Portfolio Simulation
- **Stock Selection**: Choose from 50 S&P 500 stocks
- **Allocation Sliders**: Interactive sliders for portfolio allocation (auto-normalized to 100%)
- **Portfolio Metrics**: Expected Return, Portfolio Volatility, Sharpe Ratio
- **Monte Carlo Simulation**: Run simulations with configurable parameters:
  - Number of simulations (100-1000)
  - Time period (30-365 days)
  - Initial investment amount

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit plotly pandas numpy
```

### Running the Dashboard

```bash
cd 2
python -m streamlit run sp500_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Technical Details

### Technologies Used
- **Streamlit**: Web application framework for rapid UI development
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Data Sources
- S&P 500 stock metrics including:
  - Total Return (%)
  - Annualized Return (%)
  - Volatility (%)
  - Sharpe Ratio
  - Max Drawdown (%)
  - Moving Averages (MA50, MA200)

## 💡 Key Learnings

This dashboard demonstrates:
- Building interactive data applications with Streamlit
- Creating complex financial visualizations
- Implementing portfolio optimization concepts
- Monte Carlo simulation for risk analysis
- Real-time correlation analysis

## 📁 Project Structure

```
2/
├── sp500_dashboard.py      # Main dashboard application
├── sp500_metrics.csv       # Stock performance metrics
├── sp500_correlation.csv   # Stock correlation matrix
└── README.md              # This file
```

## 🔗 Live Demo

To run locally:
```bash
cd 2
streamlit run sp500_dashboard.py
```

Then open `http://localhost:8501` in your browser.

---

**Built with ❤️ using Streamlit and Plotly**
