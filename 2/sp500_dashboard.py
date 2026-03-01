"""
S&P 500 Interactive Market Dashboard
=====================================
A comprehensive interactive dashboard for S&P 500 stock analysis including:
- Stock performance trends
- Volatility analysis
- Correlation heatmaps
- Portfolio simulation with sliders

Author: Data Scientist
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="S&P 500 Interactive Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117
    }
    .stApp {
        background-color: #0e1117
    }
    .metric-card {
        background-color: #1e2128;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00cc96;
    }
    .subtitle-text {
        font-size: 1.2rem;
        color: #8e8e8e;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the data files."""
    metrics_df = pd.read_csv('../1/sp500_metrics.csv')
    correlation_df = pd.read_csv('../1/sp500_correlation.csv')
    
    # Set ticker as index for correlation matrix
    correlation_matrix = correlation_df.set_index('Ticker')
    
    return metrics_df, correlation_matrix


def create_performance_trends(metrics_df):
    """Create stock performance trends visualization."""
    st.subheader("📊 Stock Performance Trends")
    
    # Top level metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_return = metrics_df['Total Return (%)'].mean()
        st.metric("Average Total Return", f"{avg_return:.1f}%")
    
    with col2:
        best_stock = metrics_df.loc[metrics_df['Total Return (%)'].idxmax()]
        st.metric("Best Performer", f"{best_stock['Ticker']}", f"{best_stock['Total Return (%)']:.1f}%")
    
    with col3:
        worst_stock = metrics_df.loc[metrics_df['Total Return (%)'].idxmin()]
        st.metric("Worst Performer", f"{worst_stock['Ticker']}", f"{worst_stock['Total Return (%)']:.1f}%")
    
    with col4:
        avg_volatility = metrics_df['Volatility (%)'].mean()
        st.metric("Average Volatility", f"{avg_volatility:.1f}%")
    
    # Interactive bar chart - Total Returns
    st.markdown("### Total Returns by Stock")
    
    # Sorting options
    sort_option = st.selectbox("Sort by:", ["Total Return (%)", "Annualized Return (%)", "Volatility (%)", "Sharpe Ratio"])
    n_stocks = st.slider("Number of stocks to display", 10, 50, 20, key="performance_slider")
    
    sorted_df = metrics_df.sort_values(sort_option, ascending=False).head(n_stocks)
    
    # Color based on return
    colors = ['#00cc96' if x >= 0 else '#ef553b' for x in sorted_df['Total Return (%)']]
    
    fig = px.bar(
        sorted_df,
        x='Ticker',
        y='Total Return (%)',
        color=colors,
        title=f"Top {n_stocks} Stocks by {sort_option}",
        labels={'Total Return (%)': 'Total Return (%)', 'Ticker': 'Stock'},
        color_discrete_map={'#00cc96': '#00cc96', '#ef553b': '#ef553b'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance table
    with st.expander("View Detailed Performance Table"):
        display_cols = ['Ticker', 'Total Return (%)', 'Annualized Return (%)', 
                       'Volatility (%)', 'Sharpe Ratio', 'Max Drawdown (%)']
        st.dataframe(
            metrics_df[display_cols].sort_values('Total Return (%)', ascending=False),
            use_container_width=True
        )


def create_volatility_analysis(metrics_df):
    """Create volatility analysis visualization."""
    st.subheader("📉 Volatility Analysis")
    
    # Volatility metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_vol = metrics_df[metrics_df['Volatility (%)'] > metrics_df['Volatility (%)'].median()]
        st.metric("High Volatility Stocks", len(high_vol), f"Vol > {metrics_df['Volatility (%)'].median():.1f}%")
    
    with col2:
        low_vol = metrics_df[metrics_df['Volatility (%)'] <= metrics_df['Volatility (%)'].median()]
        st.metric("Low Volatility Stocks", len(low_vol), f"Vol ≤ {metrics_df['Volatility (%)'].median():.1f}%")
    
    with col3:
        best_sharpe = metrics_df.loc[metrics_df['Sharpe Ratio'].idxmax()]
        st.metric("Best Risk-Adjusted", f"{best_sharpe['Ticker']}", f"Sharpe: {best_sharpe['Sharpe Ratio']:.2f}")
    
    # Risk-Return Scatter Plot
    st.markdown("### Risk vs Return Analysis")
    
    fig = px.scatter(
        metrics_df,
        x='Volatility (%)',
        y='Total Return (%)',
        size='Sharpe Ratio',
        color='Total Return (%)',
        hover_name='Ticker',
        hover_data=['Annualized Return (%)', 'Sharpe Ratio', 'Max Drawdown (%)'],
        color_continuous_scale='RdYlGn',
        title="Risk-Return Profile (Bubble size = Sharpe Ratio)"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Volatility (%)"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Total Return (%)")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Volatility distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = px.histogram(
            metrics_df,
            x='Volatility (%)',
            nbins=15,
            title="Volatility Distribution",
            color_discrete_sequence=['#636efa']
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Top volatile stocks
        top_volatile = metrics_df.nlargest(10, 'Volatility (%)')[['Ticker', 'Volatility (%)', 'Total Return (%)']]
        fig_bar = px.bar(
            top_volatile,
            x='Ticker',
            y='Volatility (%)',
            title="Top 10 Most Volatile Stocks",
            color='Volatility (%)',
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_bar, use_container_width=True)


def create_correlation_heatmap(correlation_matrix):
    """Create interactive correlation heatmap."""
    st.subheader("🔗 Correlation Heatmap")
    
    # Select stocks for correlation
    all_tickers = list(correlation_matrix.columns)
    selected_tickers = st.multiselect(
        "Select stocks for correlation analysis:",
        all_tickers,
        default=all_tickers[:15],
        key="corr_multiselect"
    )
    
    if selected_tickers:
        # Filter correlation matrix
        corr_subset = correlation_matrix.loc[selected_tickers, selected_tickers]
        
        # Create heatmap
        fig = px.imshow(
            corr_subset,
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            title="Stock Correlation Matrix",
            aspect="auto"
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            coloraxis_colorbar=dict(title="Correlation")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlations
        st.markdown("### Strongest Correlations")
        
        # Extract and rank correlations
        corr_pairs = []
        for i in range(len(selected_tickers)):
            for j in range(i+1, len(selected_tickers)):
                ticker1 = selected_tickers[i]
                ticker2 = selected_tickers[j]
                corr_value = corr_subset.loc[ticker1, ticker2]
                corr_pairs.append({
                    'Stock Pair': f"{ticker1} - {ticker2}",
                    'Correlation': corr_value
                })
        
        corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Positive Correlations**")
            st.dataframe(
                corr_df.head(10).style.background_gradient(cmap='Greens', subset=['Correlation']),
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Top Negative Correlations**")
            st.dataframe(
                corr_df.tail(10).sort_values('Correlation').style.background_gradient(cmap='Reds', subset=['Correlation']),
                use_container_width=True
            )


def create_portfolio_simulation(metrics_df, correlation_matrix):
    """Create portfolio simulation with sliders."""
    st.subheader("💼 Portfolio Simulation")
    
    st.markdown("""
    ### Build Your Portfolio
    Adjust the allocation sliders to see how different stock selections affect 
    your portfolio's expected return and risk.
    """)
    
    # Select stocks for portfolio
    all_tickers = list(metrics_df['Ticker'])
    portfolio_stocks = st.multiselect(
        "Select stocks for your portfolio:",
        all_tickers,
        default=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA'],
        key="portfolio_multiselect"
    )
    
    if len(portfolio_stocks) < 2:
        st.warning("Please select at least 2 stocks for portfolio analysis.")
        return
    
    # Create sliders for allocation
    st.markdown("### Allocation Sliders")
    
    # Initialize session state for allocations
    if 'allocations' not in st.session_state:
        st.session_state.allocations = {}
    
    # Equal initial allocation
    equal_weight = 100 / len(portfolio_stocks)
    
    # Create columns for sliders
    cols = st.columns(min(len(portfolio_stocks), 5))
    
    allocations = {}
    total_allocation = 0
    
    # Display sliders
    for i, ticker in enumerate(portfolio_stocks):
        with cols[i % 5]:
            # Get default value from session state or equal weight
            default_val = st.session_state.allocations.get(ticker, equal_weight)
            
            # Determine min/max based on remaining allocation
            remaining = 100 - sum([allocations.get(t, 0) for t in portfolio_stocks[:i]])
            
            allocations[ticker] = st.slider(
                f"{ticker} Allocation %",
                0.0,
                100.0,
                default_val,
                key=f"slider_{ticker}"
            )
    
    # Calculate total allocation and normalize
    total = sum(allocations.values())
    
    if total > 0:
        # Normalize allocations to 100%
        normalized_alloc = {k: (v / total) * 100 for k, v in allocations.items()}
    else:
        normalized_alloc = {k: 0 for k in allocations}
        st.warning("Please adjust allocations (total must be > 0)")
        return
    
    # Display allocation pie chart
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig_pie = px.pie(
            values=list(normalized_alloc.values()),
            names=list(normalized_alloc.keys()),
            title="Portfolio Allocation",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Calculate portfolio metrics
        portfolio_return = 0
        portfolio_variance = 0
        
        # Get metrics for selected stocks
        stock_metrics = metrics_df[metrics_df['Ticker'].isin(portfolio_stocks)].set_index('Ticker')
        
        # Calculate weighted return
        for ticker, weight in normalized_alloc.items():
            weight_decimal = weight / 100
            if ticker in stock_metrics.index:
                portfolio_return += stock_metrics.loc[ticker, 'Annualized Return (%)'] * weight_decimal
        
        # Calculate portfolio volatility using correlation matrix
        returns = []
        volatilities = []
        
        for ticker in portfolio_stocks:
            if ticker in stock_metrics.index:
                returns.append(stock_metrics.loc[ticker, 'Annualized Return (%)'])
                volatilities.append(stock_metrics.loc[ticker, 'Volatility (%)'])
        
        # Calculate portfolio variance
        weights = np.array([normalized_alloc[t] / 100 for t in portfolio_stocks if t in stock_metrics.index])
        
        # Get correlation submatrix
        corr_stocks = [t for t in portfolio_stocks if t in stock_metrics.index]
        corr_subset = correlation_matrix.loc[corr_stocks, corr_stocks]
        
        # Portfolio variance = w' * Σ * w
        vol_array = np.array(volatilities) / 100
        cov_matrix = np.outer(vol_array, vol_array) * corr_subset.values
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance) * 100
        
        # Portfolio Sharpe Ratio (assuming 5% risk-free rate)
        risk_free_rate = 5.0
        portfolio_sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        # Display metrics
        st.markdown("### Portfolio Metrics")
        
        m1, m2, m3 = st.columns(3)
        
        with m1:
            color = "#00cc96" if portfolio_return >= 0 else "#ef553b"
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #8e8e8e; margin: 0;">Expected Annual Return</h3>
                <h2 style="color: {color}; margin: 0;">{portfolio_return:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #8e8e8e; margin: 0;">Portfolio Volatility</h3>
                <h2 style="color: #ff6692; margin: 0;">{portfolio_volatility:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with m3:
            color = "#00cc96" if portfolio_sharpe >= 0 else "#ef553b"
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #8e8e8e; margin: 0;">Sharpe Ratio</h3>
                <h2 style="color: {color}; margin: 0;">{portfolio_sharpe:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Comparison with equal weight portfolio
        st.markdown("### Comparison")
        
        eq_return = stock_metrics['Annualized Return (%)'].mean()
        eq_vol = stock_metrics['Volatility (%)'].mean()
        eq_sharpe = (eq_return - risk_free_rate) / eq_vol if eq_vol > 0 else 0
        
        comp_df = pd.DataFrame({
            'Metric': ['Expected Return (%)', 'Volatility (%)', 'Sharpe Ratio'],
            'Your Portfolio': [portfolio_return, portfolio_volatility, portfolio_sharpe],
            'Equal Weight': [eq_return, eq_vol, eq_sharpe]
        })
        
        fig_comp = go.Figure(data=[
            go.Bar(name='Your Portfolio', x=comp_df['Metric'], y=comp_df['Your Portfolio'], marker_color='#636efa'),
            go.Bar(name='Equal Weight', x=comp_df['Metric'], y=comp_df['Equal Weight'], marker_color='#00cc96')
        ])
        
        fig_comp.update_layout(
            barmode='group',
            title="Portfolio Comparison",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Monte Carlo Simulation
    st.markdown("### Monte Carlo Simulation")
    
    n_simulations = st.slider("Number of simulations", 100, 1000, 500)
    n_days = st.slider("Simulation period (days)", 30, 365, 252)
    initial_investment = st.number_input("Initial investment ($)", 1000, 1000000, 10000, step=1000)
    
    if st.button("Run Simulation", key="run_sim"):
        # Run Monte Carlo simulation
        np.random.seed(42)
        
        # Daily parameters
        daily_return = portfolio_return / 252
        daily_vol = portfolio_volatility / np.sqrt(252)
        
        # Simulate paths
        sim_returns = np.zeros((n_simulations, n_days))
        
        for i in range(n_simulations):
            random_returns = np.random.normal(daily_return, daily_vol, n_days)
            sim_returns[i, :] = initial_investment * np.cumprod(1 + random_returns)
        
        # Calculate statistics
        final_values = sim_returns[:, -1]
        mean_final = np.mean(final_values)
        std_final = np.std(final_values)
        percentile_5 = np.percentile(final_values, 5)
        percentile_95 = np.percentile(final_values, 95)
        
        # Plot simulation
        fig_sim = go.Figure()
        
        # Add sample paths (limit to 50 for visibility)
        for i in range(min(50, n_simulations)):
            fig_sim.add_trace(go.Scatter(
                y=sim_returns[i, :],
                mode='lines',
                line=dict(color='rgba(99, 110, 250, 0.1)', width=1),
                showlegend=False
            ))
        
        # Add mean path
        mean_path = np.mean(sim_returns, axis=0)
        fig_sim.add_trace(go.Scatter(
            y=mean_path,
            mode='lines',
            line=dict(color='#00cc96', width=3),
            name='Mean'
        ))
        
        # Add percentile bands
        fig_sim.add_trace(go.Scatter(
            y=np.percentile(sim_returns, 5, axis=0),
            mode='lines',
            line=dict(color='#ef553b', width=1, dash='dash'),
            name='5th Percentile',
            showlegend=True
        ))
        
        fig_sim.add_trace(go.Scatter(
            y=np.percentile(sim_returns, 95, axis=0),
            mode='lines',
            line=dict(color='#00cc96', width=1, dash='dash'),
            name='95th Percentile',
            fill='tonexty',
            fillcolor='rgba(0, 204, 150, 0.1)',
            showlegend=True
        ))
        
        fig_sim.update_layout(
            title=f"Monte Carlo Simulation ({n_simulations} runs, {n_days} days)",
            xaxis_title="Days",
            yaxis_title="Portfolio Value ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_sim, use_container_width=True)
        
        # Simulation results
        res1, res2, res3, res4 = st.columns(4)
        
        with res1:
            st.metric("Mean Final Value", f"${mean_final:,.0f}")
        with res2:
            st.metric("Std Dev", f"${std_final:,.0f}")
        with res3:
            st.metric("5th Percentile", f"${percentile_5:,.0f}")
        with res4:
            st.metric("95th Percentile", f"${percentile_95:,.0f}")


def main():
    """Main dashboard function."""
    # Title
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 class="title-text">📈 S&P 500 Interactive Market Dashboard</h1>
        <p class="subtitle-text">Comprehensive stock analysis, correlation insights, and portfolio simulation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    metrics_df, correlation_matrix = load_data()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Dashboard Section:",
        ["Performance Trends", "Volatility Analysis", "Correlation Heatmap", "Portfolio Simulation"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Summary")
    st.sidebar.info(f"**Total Stocks:** {len(metrics_df)}")
    st.sidebar.info(f"**Date Range:** Recent Analysis Period")
    
    # Render selected page
    if page == "Performance Trends":
        create_performance_trends(metrics_df)
    elif page == "Volatility Analysis":
        create_volatility_analysis(metrics_df)
    elif page == "Correlation Heatmap":
        create_correlation_heatmap(correlation_matrix)
    elif page == "Portfolio Simulation":
        create_portfolio_simulation(metrics_df, correlation_matrix)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8e8e8e; padding: 20px;">
        <p>S&P 500 Interactive Dashboard | Data Analysis Project</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
