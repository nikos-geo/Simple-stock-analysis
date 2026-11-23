import yfinance as yf
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk

class BasicAnalysis:
    def __init__(self):
        # Create input box for ticker and labels

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        app = ctk.CTk()
        app.geometry('950x450')
        app.title("Basic stock analysis")
        label_style = {
            "font": ctk.CTkFont(family="Helvetica", size=12),
        }
        grid_style = {
            "padx": 10,
            "pady": 6,
        }
        ctk.CTkLabel(app, text="Stock comparison", ).grid(row=0, column=0, columnspan=4, padx=10, pady=6, sticky=W)
        ctk.CTkLabel(app, text= "Please enter the ticker you want: ", **label_style).grid(row= 2,
                                                                       column= 1, sticky=W, **grid_style)
        ctk.CTkLabel(app, text= "Daily average return: ", **label_style).grid(row= 3,
                                                                    column= 1, sticky=W, **grid_style)
        ctk.CTkLabel(app, text= "Daily standard deviation: ", **label_style).grid(row= 4,
                                                                      column= 1, sticky=W, **grid_style) 
        ctk.CTkLabel(app, text="Please select a time period: ", **label_style).grid(row=6, 
                                                                 column=1, sticky=W, **grid_style)
        ctk.CTkLabel(app, text="Correlation", **label_style).grid(row=2,
                                               column=4, **grid_style)
        ctk.CTkLabel(app, text="Total return for the period:", **label_style).grid(row=5,
                                                                column=1, sticky=W, **grid_style)
        # Take the input to display information
        self.entry1 = ctk.CTkEntry(app, placeholder_text="e.g. MSFT", justify=RIGHT, **label_style)
        self.entry1.grid(row=2, column=2, **grid_style) 

        self.entry2 = ctk.CTkEntry(app, placeholder_text="e.g. AAPL", justify=RIGHT, **label_style)
        self.entry2.grid(row=2, column=3, **grid_style)

        self.avr = StringVar()
        ctk.CTkLabel(app, textvariable=self.avr, **label_style).grid(row=3, 
                                                                       column=2, sticky=E, **grid_style)
        self.avr_2 = StringVar()
        ctk.CTkLabel(app, textvariable=self.avr_2, **label_style).grid(row=3, 
                                                                           column=3, sticky=E, **grid_style)

        self.stdDev_result = StringVar()
        ctk.CTkLabel(app, textvariable=self.stdDev_result, **label_style).grid(row=4, 
                                                                              column=2, sticky=E, **grid_style)
        self.stdDev_result_2 = StringVar()
        ctk.CTkLabel(app, textvariable=self.stdDev_result_2, **label_style).grid(row=4, 
                                                                              column=3, sticky=E, **grid_style)
        self.correl = StringVar()
        ctk.CTkLabel(app, textvariable=self.correl, **label_style).grid(row=3, 
                                                                       column=4, sticky=E, **grid_style)
        self.total_return_1 = StringVar()
        ctk.CTkLabel(app, textvariable=self.total_return_1, **label_style).grid(row=5,
                                                                              column=2, sticky=E, **grid_style)
        self.total_return_2 = StringVar()
        ctk.CTkLabel(app, textvariable=self.total_return_2, **label_style).grid(row=5,
                                                                              column=3, sticky=E, **grid_style)
        ctk.CTkLabel(app, text="Ticker 1", **label_style).grid(row=1, column=2, **grid_style)
        ctk.CTkLabel(app, text="Ticker 2", **label_style).grid(row=1, column=3, **grid_style)

        # Create the buttons to initiate the analysis and change time period and selection for csv export
        ctk.CTkButton(app, text= "See analysis",  command=self.run_analysis
                            ).grid(row=8,column=4, sticky=E, **grid_style)

        ctk.CTkButton(app, text="Export price data to csv", 
                   command=self.get_csv_data).grid(row=9, column=4, sticky=E, padx=10)
        period_choices = ("1mo", "3mo", "6mo", "1y", "max")
        self.period = StringVar(value="1mo")
        choice_box = ctk.CTkComboBox(app, variable=self.period, values=list(period_choices), 
                                  state="readonly")
        choice_box.grid(row=6, column=2, sticky=W, **grid_style)
    
        app.mainloop()

    def get_ticker_prices(self):
        """From a ticker get the prices in a data frame"""
        symbol = self.entry1.get().upper().strip()
        symbol_2 = self.entry2.get().upper().lower()
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









