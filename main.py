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

def plot_data(data, indicators, sync_axix= None):
    pass

def on_button_click(ticker1, ticker2, start, end, indicators):
    pass