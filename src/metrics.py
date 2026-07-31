import pandas as pd
import numpy as np

def calculate_current_summary(portfolio_df: pd.DataFrame, portfolio_value_df: pd.DataFrame) -> dict:
    total_invested = (portfolio_df["shares"] * portfolio_df["avg_cost"]).sum()
    current_value = portfolio_value_df["Total"].iloc[-1]
    unrealized_pnl = current_value - total_invested
    return_pct = unrealized_pnl / total_invested if total_invested != 0 else np.nan

    return {
        "total_invested": total_invested,
        "current_value": current_value,
        "unrealized_pnl": unrealized_pnl,
        "return_pct": return_pct
    }

def calculate_daily_returns(portfolio_value_df: pd.DataFrame) -> pd.Series:
    daily_returns = portfolio_value_df["Total"].pct_change().dropna()
    return daily_returns

def calculate_total_return(portfolio_value_df: pd.DataFrame) -> float:
    start_value = portfolio_value_df["Total"].iloc[0]
    end_value = portfolio_value_df["Total"].iloc[-1]

    if start_value == 0:
        return np.nan

    return (end_value / start_value) - 1

def calculate_annualized_volatility(daily_returns: pd.Series) -> float:
    if daily_returns.empty:
        return np.nan

    return daily_returns.std() * np.sqrt(252)

def calculate_drawdown_series(portfolio_value_df: pd.DataFrame) -> pd.Series:
    total_series = portfolio_value_df["Total"]
    running_max = total_series.cummax()
    drawdown = (total_series / running_max) - 1
    return drawdown

def calculate_max_drawdown(portfolio_value_df: pd.DataFrame) -> float:
    drawdown = calculate_drawdown_series(portfolio_value_df)
    return drawdown.min()