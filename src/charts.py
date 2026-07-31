import plotly.express as px
import pandas as pd

def plot_portfolio_value(portfolio_value_df: pd.DataFrame):
    fig = px.line(
        portfolio_value_df,
        x=portfolio_value_df.index,
        y="Total",
        title="Portfolio Value Over Time",
        labels={"x": "Date", "Total": "Portfolio Value"}
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    return fig

def plot_allocation_pie(portfolio_value_df: pd.DataFrame):
    latest_values = portfolio_value_df.drop(columns=["Total"]).iloc[-1]
    allocation_df = latest_values.reset_index()
    allocation_df.columns = ["Ticker", "Value"]

    fig = px.pie(
        allocation_df,
        names="Ticker",
        values="Value",
        title="Current Portfolio Allocation",
        hole=0.35
    )

    fig.update_layout(template="plotly_white")

    return fig

def plot_drawdown(drawdown_series: pd.Series):
    drawdown_df = drawdown_series.reset_index()
    drawdown_df.columns = ["Date", "Drawdown"]

    fig = px.area(
        drawdown_df,
        x="Date",
        y="Drawdown",
        title="Portfolio Drawdown",
        labels={"Drawdown": "Drawdown"}
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    return fig


def plot_benchmark_comparison(portfolio_value_df: pd.DataFrame, benchmark_series: pd.Series):

    def normalize_series(series: pd.Series) -> pd.Series:
        return 100 * series / series.iloc[0]

    portfolio_norm = normalize_series(portfolio_value_df["Total"])
    benchmark_norm = normalize_series(benchmark_series)

    comparison_df = pd.DataFrame({
        "Portfolio": portfolio_norm,
        "Benchmark": benchmark_norm
    }).reset_index()

    fig = px.line(
        comparison_df,
        x="Date",
        y=["Portfolio", "Benchmark"],
        title="Portfolio vs Benchmark",
        labels={"value": "Normalized Value", "variable": "Series"}
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    return fig