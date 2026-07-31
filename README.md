# Portfolio Tracker Dashboard

A Streamlit app for tracking portfolio value, allocation, and risk metrics.

## Features

- Upload holdings CSV (or use sample data)
- Fetch market prices with yfinance
- Track portfolio value over time
- View allocation, drawdown, and risk metrics
- Compare against a benchmark (SPY, QQQ, VTI)
- Download portfolio results as CSV

## CSV format

```csv
ticker,shares,avg_cost,buy_date
QQQ,2,500,2026-07-01
NVDA,1,140,2026-07-10
GOOGL,1,180,2026-07-15
```

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repo and push this code
2. Go to https://share.streamlit.io
3. Select your repo, branch, and `app.py`
4. Click Deploy

## Built with

- Python
- Streamlit
- yfinance
- pandas
- numpy
- plotly