import yfinance as yf
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class BasicAnalysis:
    def __init__(self):
        # Create input box for ticker and labels

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk()
        self.app.geometry('1200x950')
        self.app.title("Basic stock analysis")

        label_style = {
            "font": ctk.CTkFont(family="Helvetica", size=14),
        }
        grid_style = {
            "padx": 10,
            "pady": 6,
        }

        ctk.CTkLabel(self.app, text="Stock comparison", ).grid(row=0, column=0, columnspan=4, padx=10, pady=6, sticky=W)
        ctk.CTkLabel(self.app, text= "Please enter the ticker you want: ", **label_style).grid(row= 2,
                                                                       column= 1, sticky=W, **grid_style)
        ctk.CTkLabel(self.app, text= "Daily avg return: ", **label_style).grid(row= 3,
                                                                    column= 1, sticky=W, **grid_style)
        ctk.CTkLabel(self.app, text= "Annualized return: ", **label_style).grid(row=4, # add functionality
                                                                    column=1, sticky=W, **grid_style)
        ctk.CTkLabel(self.app, text= "Daily volatility: ", **label_style).grid(row= 5,
                                                                      column= 1, sticky=W, **grid_style) 
        ctk.CTkLabel(self.app, text="Annualized volatility: ", **label_style).grid(row=6, 
                                                                                   column=1, sticky=W, **grid_style)
        ctk.CTkLabel(self.app, text="Please select a time period: ", **label_style).grid(row=8,
                                                                 column=1, sticky=W, **grid_style)
        ctk.CTkLabel(self.app, text="Correlation", **label_style).grid(row=2,
                                               column=4, **grid_style)
        ctk.CTkLabel(self.app, text="Total return for the period:", **label_style).grid(row=7,
                                                                column=1, sticky=W, **grid_style)
        # Take the input to display information
        self.entry1 = ctk.CTkEntry(self.app, placeholder_text="e.g. MSFT", justify=RIGHT, **label_style)
        self.entry1.grid(row=2, column=2, **grid_style) 

        self.entry2 = ctk.CTkEntry(self.app, placeholder_text="e.g. AAPL", justify=RIGHT, **label_style)
        self.entry2.grid(row=2, column=3, **grid_style)

        self.avr = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.avr, **label_style).grid(row=3, 
                                                                       column=2, sticky=E, **grid_style)
        self.ann_r = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.ann_r, **label_style).grid(row=4,
                                                                            column=2, sticky=E, **grid_style)
        self.avr_2 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.avr_2, **label_style).grid(row=3, 
                                                                           column=3, sticky=E, **grid_style)
        self.ann_r2 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.ann_r2, **label_style).grid(row=4,
                                                                             column=3, sticky=E, **grid_style)

        self.stdDev_result = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.stdDev_result, **label_style).grid(row=5, 
                                                                              column=2, sticky=E, **grid_style)
        self.ann_std = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.ann_std, **label_style).grid(row=6,
                                                                              column=2, sticky= E, **grid_style)
        self.stdDev_result_2 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.stdDev_result_2, **label_style).grid(row=5, 
                                                                              column=3, sticky=E, **grid_style)
        self.ann_std2 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.ann_std2, **label_style).grid(row=6, 
                                                                               column=3, sticky=E, **grid_style)
        self.correl = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.correl, **label_style).grid(row=3, 
                                                                       column=4, sticky=E, **grid_style)
        self.total_return_1 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.total_return_1, **label_style).grid(row=7,
                                                                              column=2, sticky=E, **grid_style)
        self.total_return_2 = StringVar()
        ctk.CTkLabel(self.app, textvariable=self.total_return_2, **label_style).grid(row=7,
                                                                              column=3, sticky=E, **grid_style)
        ctk.CTkLabel(self.app, text="Ticker 1", **label_style).grid(row=1, column=2, **grid_style)
        ctk.CTkLabel(self.app, text="Ticker 2", **label_style).grid(row=1, column=3, **grid_style)

        # Create the buttons to initiate the analysis and change time period and selection for csv export
        ctk.CTkButton(self.app, text= "See analysis",  command=self.run_analysis
                            ).grid(row=9,column=4, sticky=E, **grid_style)

        ctk.CTkButton(self.app, text="Export price data to csv", 
                   command=self.get_csv_data).grid(row=9, column=5, sticky=E, **grid_style)
        period_choices = ("1mo", "3mo", "6mo", "1y", "max")
        self.period = StringVar(value="1mo")
        choice_box = ctk.CTkComboBox(self.app, variable=self.period, values=list(period_choices), 
                                  state="readonly")
        choice_box.grid(row=8, column=2, sticky=W, **grid_style)

        # Creat the figure and the canvas for the plotting
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.app,)
        self.plot1 = self.fig.add_subplot(111)

        # Create the slider for the portfolio weights
        ctk.CTkLabel(self.app, text="Adjust 2 stock portfolio weights", **label_style).grid(row=9,
                                                                                            column=1, **grid_style)
        self.slider = ctk.CTkSlider(self.app, from_=0, to=1, number_of_steps=100,
                                    command=self.calculate_portfolio_weights)
        self.slider.set(0.5)
        self.slider.grid(row=9,column=2, sticky=W, **grid_style)
        self.weight_text = StringVar(value="Ticker 1 50% / Ticker 2 50%")
        ctk.CTkLabel(self.app, textvariable=self.weight_text, **label_style).grid(row=9, column=3, sticky=W, **grid_style)

        # Add labels for portfolio return
        
        ctk.CTkLabel(self.app, text="Portfolio return: ", **label_style).grid(row=10, 
                                                                              column=1, sticky=W, **grid_style)
        self.port_return = StringVar()
        ctk.CTkLabel(self.app, textvariable= self.port_return, **label_style).grid(row=10, 
                                                                                   column=2, **grid_style)

        ctk.CTkLabel(self.app, text="Portfolio volatility: ", **label_style).grid(row=11, 
                                                                              column=1, sticky=W, **grid_style)
        self.port_volatility = StringVar()
        ctk.CTkLabel(self.app, textvariable= self.port_volatility, **label_style).grid(row=11, 
                                                                                   column=2, **grid_style)
    
        self.app.mainloop()

    def _plot_colors(self):
        if ctk.get_appearance_mode() == "Dark":
            return {"bg": "#2B2B2B", "fg": "#DCE4EE"}
        return {"bg": "#EBEBEB", "fg": "#1A1A1A"}

    def get_ticker_prices(self):
        """From a ticker get the prices in a data frame"""
        symbol = self.entry1.get().upper().strip()
        symbol_2 = self.entry2.get().upper().strip()
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
            return prices, prices_2, symbol, symbol_2
        
    def calculate_returns(self):
        """Calculate the returns """
        data = self.get_ticker_prices()
        if data is None:
            return
        prices_tick_1, prices_tick_2, symbol, symbol2 = data
        total_return_1 = ((prices_tick_1.iloc[-1] - prices_tick_1.iloc[0]) / prices_tick_1.iloc[0]) * 100
        total_return_2 = ((prices_tick_2.iloc[-1] - prices_tick_2.iloc[0]) / prices_tick_2.iloc[0]) * 100
        norm1 = prices_tick_1 / prices_tick_1.iloc[0] * 100
        norm2 = prices_tick_2 / prices_tick_2.iloc[0] * 100 
        return (prices_tick_1.pct_change().dropna() * 100, prices_tick_2.pct_change().dropna() * 100, total_return_1, total_return_2, norm1, norm2,
                symbol, symbol2)
        
    def run_analysis(self):
        """Run all calculations and return them in appropriate boxes"""
        data = self.calculate_returns()
        if data is None:
            return
        r1, r2, tr1, tr2, norm1, norm2, symbol, symbol2 = data
        average_r1 = np.average(r1)
        annual_r1 = average_r1 * 252
        average_r2 = np.average(r2)
        annual_r2 = average_r2 * 252
        std_1 = np.std(r1, ddof= 1)
        annual_std1 = std_1 * np.sqrt(252)
        std_2 = np.std(r2, ddof= 1)
        annual_std2 = std_2 * np.sqrt(252)
        self.avr.set(f'{average_r1:.2f}%')
        self.ann_r.set(f'{annual_r1:.2f}%')
        self.avr_2.set(f'{average_r2:.2f}%')
        self.ann_r2.set(f'{annual_r2:.2f}%')

        self.stdDev_result.set(f'{std_1:.2f}%')
        self.ann_std.set(f'{annual_std1:.2f}%')
        self.stdDev_result_2.set(f'{std_2:.2f}%')
        self.ann_std2.set(f'{annual_std2:.2f}%')

        p1 = norm1.copy()
        p2 = norm2.copy()

        p1.index = p1.index.tz_localize(None).normalize()
        p2.index = p2.index.tz_localize(None).normalize()
        aligned = pd.concat([p1, p2], axis=1, join="inner")
        aligned_returns = aligned.pct_change().dropna()
        correlation = aligned_returns.iloc[:, 0].corr(aligned_returns.iloc[:, 1])
        n_obs = len(aligned_returns)

        if n_obs < 3 or pd.isna(correlation):
            self.correl.set("N/A")
        else:
            self.correl.set(f'{correlation:.2f} (n={n_obs})')

        self.total_return_1.set(f'{tr1:.2f}%')
        self.total_return_2.set(f'{tr2:.2f}%')

        # Make the plot
        c = self._plot_colors()
        self.plot1.clear()
        self.fig.set_facecolor(c["bg"])
        self.plot1.set_facecolor(c["bg"])

        self.plot1.plot(norm1, color='#3B8ED0', linewidth=1, label=f"{symbol.upper()}")
        self.plot1.plot(norm2, color="#F39C4A", linewidth=1, label=f"{symbol2.upper()}")
        self.plot1.set_ylabel("Normalized prices", color=c["fg"])
        for side in ("bottom", "top", "right", "left"):
            self.plot1.spines[side].set_color(c["fg"])
        self.plot1.axes.get_xaxis().set_ticks([])
        self.plot1.tick_params(axis='y', colors=c["fg"], labelsize=11)
        self.plot1.legend(frameon=False, labelcolor=c["fg"])
        
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=14, column=1, rowspan=10, columnspan=3, sticky=NSEW, padx=10, pady=6)

        data_w = self.calculate_portfolio_weights(self.slider.get())
        w1, w2 = data_w
        portfolio_r = (w1 * annual_r1) + (w2 * annual_r2)
        portfolio_v = np.sqrt((w1 ** 2) * (annual_std1 ** 2 ) + (w2 ** 2) * (annual_std2 ** 2) + (correlation * 2 * w1 * w2 * annual_std1 * annual_std2))
        self.port_return.set(f'{portfolio_r:.2f}%')
        self.port_volatility.set(f'{portfolio_v:.2f}%')
        
        return average_r1, average_r2, std_1, std_2, correlation, tr1, tr2

    def get_csv_data(self):
        """The function for getting the returns on a csv file"""
        data = self.get_ticker_prices()
        if data is None:
            return
        else:
            prices1, prices2, symbol, symbol2 = data
            df = pd.DataFrame()
            df[f'{symbol}'] = prices1
            df[f'{symbol2}'] = prices2
            df.to_csv("price_data_file.csv")

    def calculate_portfolio_weights(self, value):
        """Determine the weights based on user input """
        w1 = value
        w2 = 1 - value
        t1 = self.entry1.get().upper().strip() or "Ticker 1"
        t2 = self.entry2.get().upper().strip() or "Ticker 2"
        self.weight_text.set(f"{t1} {w1:.0%} / {t2} {w2:.0%}")
        return w1, w2
            
if __name__ == "__main__":
    BasicAnalysis()









