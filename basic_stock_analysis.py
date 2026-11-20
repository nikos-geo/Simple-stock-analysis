import yfinance as yf
import numpy as np
import csv
import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk

class BasicAnalysis:
    def __init__(self):
        window = Tk()
        window.geometry('850x400') # Sets apropriate window size
        window.title("Basic stock analysis") 
        window.configure(bg="#1e1f26")
        # Create input box for ticker and labels
        label_style= {
            "font": ("Helvetica", 12),
            "bg": "#1e1f26",
            "fg": "white"
        }
        Label(window, text= "Please enter the ticker you want: ", **label_style).grid(row= 2,
                                                                       column= 1, sticky=W)
        Label(window, text= "Daily average return: ", **label_style).grid(row= 3,
                                                                    column= 1, sticky=W)
        Label(window, text= "Daily standard deviation: ", **label_style).grid(row= 4,
                                                                      column= 1, sticky=W) 
        Label(window, text="Please select a time period: ", **label_style).grid(row=7, 
                                                                 column=1, sticky=W)
        Label(window, text="Correlation", **label_style).grid(row=2,
                                               column=4,)
        Label(window, text="Total return for the period:", **label_style).grid(row=6,
                                                                column=1, sticky=W)
        # Take the input to display information
        self.an_ticker = StringVar()
        Entry(window, textvariable= self.an_ticker, justify=RIGHT, bg="#595c6e", fg="white").grid(row=2, column=2) 

        self.an_ticker_2 = StringVar()
        Entry(window, textvariable= self.an_ticker_2, justify=RIGHT, bg="#595c6e", fg="white").grid(row=2, column=3)

        self.avr = StringVar()
        Label(window, textvariable=self.avr, fg="white", bg="#1e1f26").grid(row=3, 
                                                                       column=2, sticky=E)
        self.avr_2 = StringVar()
        Label(window, textvariable=self.avr_2, fg="white", bg="#1e1f26").grid(row=3, 
                                                                           column=3, sticky=E)

        self.stdDev_result = StringVar()
        Label(window, textvariable=self.stdDev_result, fg="white", bg="#1e1f26").grid(row=4, 
                                                                              column=2, sticky=E)
        self.stdDev_result_2 = StringVar()
        Label(window, textvariable=self.stdDev_result_2, fg="white", bg="#1e1f26").grid(row=4, 
                                                                              column=3, sticky=E)
        self.correl = StringVar()
        Label(window, textvariable=self.correl, fg="white", bg="#1e1f26").grid(row=3, 
                                                                       column=4, sticky=E)
        self.total_return_1 = StringVar()
        Label(window, textvariable=self.total_return_1, fg="white", bg="#1e1f26").grid(row=6,
                                                                              column=2, sticky=E)
        self.total_return_2 = StringVar()
        Label(window, textvariable=self.total_return_2, fg="white", bg="#1e1f26").grid(row=6,
                                                                              column=3, sticky=E)
        Label(window, text="Ticker 1").grid(row=1, column=2)
        Label(window, text="Ticker 2").grid(row=1, column=3)

        # Create the buttons to initiate the analysis and change time period and selection for csv export
        Button(window, text= "See analysis",  command=self.run_analysis
                            ).grid(row=8,column=4, sticky=E,)

        Button(window, text="Export price data to csv", 
                   command=self.get_csv_data).grid(row=9, column=4, sticky=E)
        period_choices = ("1mo", "3mo", "6mo", "1y", "max")
        self.period = StringVar(value="1mo")
        choice_box = ttk.Combobox(window, textvariable=self.period, values=period_choices, 
                                  state="readonly")
        choice_box.grid(row=7, column=2, sticky=W)
    
        window.mainloop()

    def get_ticker_prices(self):
        """From a ticker get the prices in a data frame"""
        symbol = self.an_ticker.get().upper().strip()
        symbol_2 = self.an_ticker_2.get().upper().strip()
        t_period = self.period.get()
        ticker = yf.Ticker(symbol)
        ticker_2 = yf.Ticker(symbol_2)
        df = ticker.history(period= t_period)
        df_2 = ticker_2.history(period= t_period)
        prices = df["Close"]
        prices_2 = df_2["Close"]
        if prices.empty or prices_2.empty:
            messagebox.showerror(icon="warning", title="Ticker error", 
                                 message="Invalid ticker, please try again.")
            return None
        else:
            return prices, prices_2
        
    def calculate_returns(self):
        """Calculate the returns """
        data = self.get_ticker_prices()
        if data is None:
            return
        prices_tick_1, prices_tick_2 = data
        total_return_1 = ((prices_tick_1.iloc[-1] - prices_tick_1.iloc[0]) / prices_tick_1.iloc[0]) * 100
        total_return_2 = ((prices_tick_2.iloc[-1] - prices_tick_2.iloc[0]) / prices_tick_2.iloc[0]) * 100
        return prices_tick_1.pct_change().dropna() * 100, prices_tick_2.pct_change().dropna() * 100, total_return_1, total_return_2
 
    def run_analysis(self):
        """Run all calculations and return them in appropriate boxes"""
        data = self.calculate_returns()
        if data is None:
            return
        r1, r2, tr1, tr2 = data
        average_r1 = np.average(r1)
        average_r2 = np.average(r2)
        std_1 = np.std(r1, ddof= 1)
        std_2 = np.std(r2, ddof= 1)
        self.avr.set(f'{average_r1:.2f}%')
        self.avr_2.set(f'{average_r2:.2f}%')

        self.stdDev_result.set(f'{std_1:.2f}%')
        self.stdDev_result_2.set(f'{std_2:.2f}%')

        r1.index = r1.index.tz_localize(None).normalize()
        r2.index = r2.index.tz_localize(None).normalize()
        correlation = r1.corr(r2)
        self.correl.set(f'{correlation:.2f}')

        self.total_return_1.set(f'{tr1:.2f}%')
        self.total_return_2.set(f'{tr2:.2f}%')
        return average_r1, average_r2, std_1, std_2, correlation, tr1, tr2

    def get_csv_data(self):
        """The function for getting the returns on a csv file"""
        data = self.get_ticker_prices()
        if data is None:
            return
        else:
            df = pd.DataFrame(data)
            df.T.to_csv("price_data_file.csv")
            




if __name__ == "__main__":
    BasicAnalysis()









