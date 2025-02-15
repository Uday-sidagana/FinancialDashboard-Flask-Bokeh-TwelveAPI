import math
import numpy as np
import datetime as dt

import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import buttons, TextInput, DatePicker, MultiChoice
from bokeh.layouts import column, row


def load_data(ticker1, ticker2, start, end): 
    # Ticker = Financial abbreviation ex. Axiom is abbreviated as XOM
    df1= yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)
    return df1, df2

def plot_data(data, indicators, sync_axis= None):
    pass

def on_button_click(ticker1, ticker2, start, end, indicators):
    pass

stock1_text = TextInput(title = "Stock 1")
stock2_text = TextInput(title = "Stock 2")

date_picker_from = DatePicker(title = "Start Date", value ="2020-01-01", min_date='2000-01-01', 
                              max_date=dt.datetime.now().strftime("%Y-%M-%D"))

date_picker_to = DatePicker(title = "End Date", value ="2020-02-01", min_date='2000-01-01', 
                            max_date=dt.datetime.now().strftime("%Y-%M-%D"))