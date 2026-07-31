import pandas as pd
from pypfopt import EfficientFrontier, expected_returns
from pypfopt.risk_models import CovarianceShrinkage

def prepare_price_data(price_df: pd.DataFrame) -> pd.DataFrame:
    clean_df = price_df.dropna(axis=1, how="all").dropna()
    return clean_df

def estimate_mu_and_cov(price_df: pd.DataFrame):
    mu = expected_returns.mean_historical_return(price_df)
    S = CovarianceShrinkage(price_df).ledoit_wolf()
    return mu, S

def optimize_min_vol(price_df: pd.DataFrame, weight_bounds=(0, 0.4)):
    price_df = prepare_price_data(price_df)
    mu, S = estimate_mu_and_cov(price_df)

    ef = EfficientFrontier(mu, S, weight_bounds=weight_bounds)
    ef.min_volatility()
    weights = ef.clean_weights()
    perf = ef.portfolio_performance(verbose=False)

    return weights, perf

def optimize_max_sharpe(price_df: pd.DataFrame, weight_bounds=(0, 0.4), risk_free_rate=0.02):
    price_df = prepare_price_data(price_df)
    mu, S = estimate_mu_and_cov(price_df)

    ef = EfficientFrontier(mu, S, weight_bounds=weight_bounds)
    ef.max_sharpe(risk_free_rate=risk_free_rate)
    weights = ef.clean_weights()
    perf = ef.portfolio_performance(verbose=False, risk_free_rate=risk_free_rate)

    return weights, perf

def weights_to_dataframe(weights: dict) -> pd.DataFrame:
    df = pd.DataFrame(
        [{"Ticker": k, "Weight": v} for k, v in weights.items() if v > 0]
    )
    if not df.empty:
        df["Weight %"] = df["Weight"] * 100
        df = df.sort_values("Weight", ascending=False).reset_index(drop=True)
    return df