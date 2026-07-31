# Portfolio Tracker Dashboard

A Streamlit app for tracking portfolio value, allocation, and risk metrics.

## Features

- Upload holdings CSV (or use sample data)
- Fetch market prices with yfinance
- Track portfolio value over time
- View allocation, drawdown, and risk metrics
- Compare against a benchmark (SPY, QQQ, VTI)
- Download portfolio results as CSV
- Explore simple portfolio optimization with valid Yahoo Finance tickers

## CSV format

```csv
ticker,shares,avg_cost,buy_date
QQQ,2,500,2026-07-01
NVDA,1,140,2026-07-10
GOOGL,1,180,2026-07-15
```

## Simple user guide

### 1. How to make the CSV

Create a CSV file with these 4 columns:

- `ticker` = stock or ETF ticker, for example `QQQ`, `NVDA`, `AAPL`, `VXUS`
- `shares` = how many shares you own
- `avg_cost` = your average buy price
- `buy_date` = purchase date in `YYYY-MM-DD` format

You can make the file in:

- **Excel**: create the table, then save as CSV
- **Google Sheets**: create the table, then download as CSV
- **VS Code / Notepad**: paste plain text and save as `.csv`

Example:

```csv
ticker,shares,avg_cost,buy_date
AAPL,2,210,2026-07-01
MSFT,1,500,2026-07-05
QQQ,3,520,2026-07-10
```

### 2. How to find tickers

Use valid Yahoo Finance tickers.

Examples:

- `AAPL` = Apple
- `QQQ` = Invesco QQQ ETF
- `VXUS` = Vanguard Total International Stock ETF
- `0700.HK` = Tencent on Yahoo Finance

If you are unsure, search the company or ETF name on Yahoo Finance and copy the exact ticker shown.

### 3. How to use the Tracker

1. Run the app.
2. Open the **Tracker** tab.
3. Upload your CSV file, or use the sample data.
4. Choose a start date and end date.
5. Choose a benchmark like `SPY`, `QQQ`, or `VTI`.
6. Review the results.

The Tracker shows:

- total invested
- current value
- unrealized profit and loss
- return vs cost
- annualized volatility
- max drawdown
- portfolio chart
- benchmark comparison
- allocation chart
- downloadable CSV outputs

### 4. How to use the Optimizer

1. Open the **Optimizer** tab.
2. Enter 2 or more valid Yahoo Finance tickers separated by commas.
3. Example:

```text
SPY,QQQ,VTI,VXUS,BND
```

4. Choose the start date and end date.
5. Choose an objective:
   - `Max Sharpe`
   - `Min Volatility`
6. Set the max weight per asset.
7. If needed, adjust the risk-free rate.
8. Review the suggested weights and metrics.

The Optimizer shows:

- expected annual return
- annual volatility
- Sharpe ratio
- suggested portfolio weights
- allocation pie chart

### 5. Notes

- Tickers must be valid Yahoo Finance symbols.
- The tracker uses a CSV because it reads your holdings from that file.
- The optimizer does not need a CSV; it uses the tickers you type in.
- Optimization results are educational and based on historical data.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repo and push this code
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Select your repo, branch, and `app.py`
4. Click Deploy

## Built with

- Python
- Streamlit
- yfinance
- pandas
- numpy
- plotly
- PyPortfolioOpt

Market data is fetched from Yahoo Finance via yfinance.