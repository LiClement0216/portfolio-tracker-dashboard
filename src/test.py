from pathlib import Path
from data import load_portfolio, fetch_price_data, build_portfolio_value_series
from metrics import calculate_drawdown_series
from charts import plot_portfolio_value, plot_allocation_pie, plot_drawdown

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "sample_portfolio.csv"

portfolio_df = load_portfolio(csv_path)
tickers = portfolio_df["ticker"].tolist()
price_df = fetch_price_data(tickers, "2026-07-01", "2026-07-31")
portfolio_value_df = build_portfolio_value_series(portfolio_df, price_df)

drawdown_series = calculate_drawdown_series(portfolio_value_df)

fig1 = plot_portfolio_value(portfolio_value_df)
fig2 = plot_allocation_pie(portfolio_value_df)
fig3 = plot_drawdown(drawdown_series)

fig1.show()
fig2.show()
fig3.show()