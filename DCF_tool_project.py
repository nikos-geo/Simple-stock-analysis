import yfinance as yf
import math 

def get_latest_fcf(ticker):
    """Get a ticker from the user"""
    try:
        symbol = yf.Ticker(ticker)
        fcf = symbol.cashflow.loc["Free Cash Flow"]
        r_fcf = fcf.iloc[0]
    except Exception as e:
        return f"No data could be fetched for {ticker}"
    return float(r_fcf)
    

   
    

while True:
    ticker_choice = input("Please enter a valid ticker: ").upper()
    print(get_latest_fcf(ticker_choice))
    break




        
  
        



