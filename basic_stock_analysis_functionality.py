import yfinance as yf




def get_ticker():
    """From a ticker get the prices for the past month in a data frame"""
    symbol = input("Please enter a valid ticker symbol: ").strip().upper()
    ticker = yf.Ticker(symbol)
    df = ticker.history(period= "1mo")
    prices = df["Close"]
    return prices

def calculate_average_return():
    """Calculate last months returns and store them in a list"""
    x = 0
    df = get_ticker()
    df_p = []
    while x < len(df) - 1:
        y = df.iloc[x]
        z = df.iloc[x + 1]
        r = float(((z - y) / y) * 100)
        df_p.append(r)
        x = x + 1

    total = 0
    for ret in df_p:
        total = total + ret

    average_r = total / len(df_p)
    return average_r

print(calculate_average_return())

        



    

