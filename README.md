# Simple-stock-analysis

A small desktop app (Python + Tkinter) that compares two stocks side by side. Enter two tickers, pick a time period, and get each stock's average daily return, volatility, total return, and how closely the two move together. You can also export the closing prices to a CSV file.

Price data is pulled from Yahoo Finance through the [`yfinance`](https://github.com/ranaroussi/yfinance) library.

Features

- Compare two tickers at the same time
- Choose a period: `1mo`, `3mo`, `6mo`, `1y` or `max`
- Calculates, for each ticker:
  - Daily average return
  - Daily standard deviation
  - Total return for the period
- Calculates the correlation between the two tickers' daily returns
- Exports closing prices to `price_data_file.csv`
- Dark-themed GUI built with Tkinter
- Shows an error popup if a ticker is invalid

Requirements

- Python 3.8+
- yfinance
- numpy
- pandas
- Tkinter 

Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install yfinance numpy pandas
```
Usage

```bash
python basic_analysis.py
```

> Replace `basic_analysis.py` with whatever you named the script.

1. Type a ticker in the Ticker 1 box and another in the Ticker 2 box (e.g. `AAPL` and `MSFT`). Both are required.
2. Select a time period from the dropdown (default is `1mo`).
3. Click See analysis to fill in the results.
4. Click Export price data to csv to save the closing prices.
