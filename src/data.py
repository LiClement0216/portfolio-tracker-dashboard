import yfinance as yf
import pandas as pd
from pathlib import Path

def load_portfolio(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required_cols = ["ticker", "shares", "avg_cost", "buy_date"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["shares"] = pd.to_numeric(df["shares"], errors="coerce")
    df["avg_cost"] = pd.to_numeric(df["avg_cost"], errors="coerce")
    df["buy_date"] = pd.to_datetime(df["buy_date"], errors="coerce")

    df = df.dropna(subset=["ticker", "shares", "avg_cost", "buy_date"])

    return df

def fetch_price_data(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    if not tickers:
        raise ValueError("Ticker list is empty.")

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        raise ValueError("No price data returned from yfinance.")

    if len(tickers) == 1:
        price_df = data[["Close"]].copy()
        price_df.columns = tickers
    else:
        price_df = data["Close"].copy()

    price_df = price_df.sort_index()
    price_df = price_df.ffill().dropna(how="all")

    return price_df

def build_portfolio_value_series(portfolio_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    shares_map = portfolio_df.set_index("ticker")["shares"]

    common_tickers = [ticker for ticker in shares_map.index if ticker in price_df.columns]
    if not common_tickers:
        raise ValueError("No matching tickers between portfolio and price data.")

    aligned_prices = price_df[common_tickers].copy()
    aligned_shares = shares_map[common_tickers]

    position_values = aligned_prices.mul(aligned_shares, axis=1)
    total_portfolio_value = position_values.sum(axis=1)

    result = position_values.copy()
    result["Total"] = total_portfolio_value

    return result

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    csv_path = BASE_DIR / "sample_portfolio.csv"

    portfolio_df = load_portfolio(csv_path)
    tickers = portfolio_df["ticker"].tolist()
    price_df = fetch_price_data(tickers, "2026-07-01", "2026-07-31")
    portfolio_value_df = build_portfolio_value_series(portfolio_df, price_df)

    print(portfolio_value_df.tail())