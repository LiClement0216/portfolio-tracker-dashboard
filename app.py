from pathlib import Path
import streamlit as st
import pandas as pd

from src.data import load_portfolio, fetch_price_data, build_portfolio_value_series
from src.metrics import (
    calculate_current_summary,
    calculate_daily_returns,
    calculate_total_return,
    calculate_annualized_volatility,
    calculate_drawdown_series,
    calculate_max_drawdown
)
from src.charts import (
    plot_portfolio_value,
    plot_allocation_pie,
    plot_drawdown,
    plot_benchmark_comparison,
    plot_weights_pie
)
from src.optimizer import (
    optimize_min_vol,
    optimize_max_sharpe,
    weights_to_dataframe
)

st.set_page_config(
    page_title="Portfolio Tracker Dashboard",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = BASE_DIR / "sample_portfolio.csv"

@st.cache_data
def cached_load_portfolio(path):
    return load_portfolio(path)

@st.cache_data(ttl=3600)
def cached_fetch_price_data(tickers, start_date, end_date):
    return fetch_price_data(list(tickers), start_date, end_date)

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=True).encode("utf-8")

st.title("Portfolio Tracker Dashboard")
st.caption("Track portfolio value, allocation, risk, and simple portfolio optimization.")

tracker_tab, optimizer_tab = st.tabs(["Tracker", "Optimizer"])

with tracker_tab:
    with st.sidebar:
        st.header("Tracker Inputs")

        uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])
        start_date = st.date_input("Start date", value=pd.to_datetime("2026-07-01"), key="tracker_start")
        end_date = st.date_input("End date", value=pd.to_datetime("2026-07-31"), key="tracker_end")
        benchmark_ticker = st.selectbox("Benchmark", options=["SPY", "QQQ", "VTI"], index=0, key="tracker_benchmark")

        st.markdown("### Current CSV format")
        st.code("ticker,shares,avg_cost,buy_date", language="text")

    try:
        if uploaded_file is not None:
            portfolio_df = pd.read_csv(uploaded_file)
            portfolio_df["ticker"] = portfolio_df["ticker"].astype(str).str.upper().str.strip()
            portfolio_df["shares"] = pd.to_numeric(portfolio_df["shares"], errors="coerce")
            portfolio_df["avg_cost"] = pd.to_numeric(portfolio_df["avg_cost"], errors="coerce")
            portfolio_df["buy_date"] = pd.to_datetime(portfolio_df["buy_date"], errors="coerce")
            portfolio_df = portfolio_df.dropna(subset=["ticker", "shares", "avg_cost", "buy_date"])
        else:
            portfolio_df = cached_load_portfolio(str(DEFAULT_CSV))

        tickers = portfolio_df["ticker"].tolist()

        price_df = cached_fetch_price_data(
            tuple(tickers),
            str(start_date),
            str(end_date)
        )

        benchmark_price_df = cached_fetch_price_data(
            (benchmark_ticker,),
            str(start_date),
            str(end_date)
        )
        benchmark_series = benchmark_price_df[benchmark_ticker]

        portfolio_value_df = build_portfolio_value_series(portfolio_df, price_df)

        summary = calculate_current_summary(portfolio_df, portfolio_value_df)
        daily_returns = calculate_daily_returns(portfolio_value_df)
        total_return = calculate_total_return(portfolio_value_df)
        annualized_volatility = calculate_annualized_volatility(daily_returns)
        drawdown_series = calculate_drawdown_series(portfolio_value_df)
        max_drawdown = calculate_max_drawdown(portfolio_value_df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Invested", f"${summary['total_invested']:,.2f}")
        col2.metric("Current Value", f"${summary['current_value']:,.2f}")
        col3.metric("Unrealized PnL", f"${summary['unrealized_pnl']:,.2f}")
        col4.metric("Return vs Cost", f"{summary['return_pct'] * 100:.2f}%")

        col5, col6, col7 = st.columns(3)
        col5.metric("Period Return", f"{total_return * 100:.2f}%")
        col6.metric("Annualized Volatility", f"{annualized_volatility * 100:.2f}%")
        col7.metric("Max Drawdown", f"{max_drawdown * 100:.2f}%")

        st.plotly_chart(plot_portfolio_value(portfolio_value_df), use_container_width=True)

        st.plotly_chart(
            plot_benchmark_comparison(portfolio_value_df, benchmark_series),
            use_container_width=True
        )

        left_col, right_col = st.columns(2)
        with left_col:
            st.plotly_chart(plot_allocation_pie(portfolio_value_df), use_container_width=True)

        with right_col:
            st.plotly_chart(plot_drawdown(drawdown_series), use_container_width=True)

        st.subheader("Holdings")
        st.dataframe(portfolio_df, use_container_width=True)

        st.subheader("Portfolio Value Table")
        st.dataframe(portfolio_value_df.tail(20), use_container_width=True)

        st.subheader("Downloads")

        holdings_csv = portfolio_df.to_csv(index=False).encode("utf-8")
        portfolio_value_csv = convert_df_to_csv(portfolio_value_df)

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            st.download_button(
                label="Download holdings CSV",
                data=holdings_csv,
                file_name="holdings.csv",
                mime="text/csv"
            )

        with download_col2:
            st.download_button(
                label="Download portfolio value CSV",
                data=portfolio_value_csv,
                file_name="portfolio_value.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Tracker error: {e}")

with optimizer_tab:
    st.subheader("Portfolio Optimizer")
    st.caption("Educational optimizer based on historical returns and covariance.")

    optimizer_ticker_input = st.text_input(
        "Candidate tickers (comma-separated)",
        value="SPY,QQQ,VTI,VXUS,BND"
    )

    optimizer_start_date = st.date_input(
        "Optimizer start date",
        value=pd.to_datetime("2024-01-01"),
        key="optimizer_start"
    )

    optimizer_end_date = st.date_input(
        "Optimizer end date",
        value=pd.to_datetime("2026-07-31"),
        key="optimizer_end"
    )

    objective = st.selectbox(
        "Objective",
        options=["Max Sharpe", "Min Volatility"],
        index=0
    )

    max_weight_pct = st.slider(
        "Max weight per asset (%)",
        min_value=10,
        max_value=100,
        value=40,
        step=5
    )

    risk_free_rate = st.number_input(
        "Risk-free rate",
        min_value=0.0,
        max_value=0.10,
        value=0.02,
        step=0.005
    )

    optimizer_tickers = [t.strip().upper() for t in optimizer_ticker_input.split(",") if t.strip()]

    if len(optimizer_tickers) < 2:
        st.warning("Please enter at least 2 tickers.")
    else:
        try:
            optimizer_price_df = cached_fetch_price_data(
                tuple(optimizer_tickers),
                str(optimizer_start_date),
                str(optimizer_end_date)
            )

            weight_bounds = (0, max_weight_pct / 100)

            if objective == "Max Sharpe":
                weights, perf = optimize_max_sharpe(
                    optimizer_price_df,
                    weight_bounds=weight_bounds,
                    risk_free_rate=risk_free_rate
                )
                chart_title = "Max Sharpe Allocation"
            else:
                weights, perf = optimize_min_vol(
                    optimizer_price_df,
                    weight_bounds=weight_bounds
                )
                chart_title = "Minimum Volatility Allocation"

            weights_df = weights_to_dataframe(weights)

            expected_return, annual_volatility, sharpe_ratio = perf

            m1, m2, m3 = st.columns(3)
            m1.metric("Expected Annual Return", f"{expected_return * 100:.2f}%")
            m2.metric("Annual Volatility", f"{annual_volatility * 100:.2f}%")
            m3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

            left_col, right_col = st.columns(2)

            with left_col:
                st.plotly_chart(
                    plot_weights_pie(weights_df, title=chart_title),
                    use_container_width=True
                )

            with right_col:
                display_df = weights_df.copy()
                if not display_df.empty:
                    display_df["Weight %"] = display_df["Weight %"].map(lambda x: f"{x:.2f}%")
                    st.dataframe(display_df[["Ticker", "Weight %"]], use_container_width=True)
                else:
                    st.warning("No valid weights returned.")

        except Exception as e:
            st.error(f"Optimizer error: {e}")