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
    df = data
    gain = df.Close> df.Open
    loss = df.Close< df.Open
    width = 12*60*60*1000

    if sync_axis is not None:
        p = figure(tools="pan, wheel_zoom,box_zoom, reset,save", 
                   x_axis_type="datetime", width= 1000, x_range = sync_axis)
        
    else:
        p = figure(tools='pan, wheel_zoom,box_zoom,reset,save', 
                   x_axis_type='datetime', width=1000)

    p.xaxis.major_label_orientation = math.pi/4
    p.grid.grid_line_alpha = 0.25
    p.segment(df.index, df.High, df.index, df.Low, color="black")

    p.vbar(df.index[gain], width, df.Open[gain], df.Close[gain], fill_color="00ff00", line_color="00ff00")
    p.vbar(df.index[loss], width, df.Open[loss], df.Close[loss], fill_color="ff0000", line_color="ff0000")

    return p



def on_button_click(ticker1, ticker2, start, end, indicators):
    df1, df2 = load_data(ticker1, ticker2, start, end)
    p1= plot_data(df1, indicators)
    p2= plot_data(df2, indicators, sync_axis=p1.x_range)
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))


#UI LAYOUT(Choosing start date, end, Text, Labels, indicators and buttons)

stock1_text = TextInput(title = "Stock 1")
stock2_text = TextInput(title = "Stock 2")

date_picker_from = DatePicker(title = "Start Date", value ="2020-01-01", min_date='2000-01-01', 
                              max_date=dt.datetime.now().strftime("%Y-%M-%D"))

date_picker_to = DatePicker(title = "End Date", value ="2020-02-01", min_date='2000-01-01', 
                            max_date=dt.datetime.now().strftime("%Y-%M-%D"))

indicator_choice = MultiChoice(options =["100 DAY SMA", "30 DAY SMA", "Linear Regression Line"])

load_button = buttons(label = "Load Data", button_type ='success')

load_button.on_click(on_button_click(stock1_text.value, stock2_text.value, date_picker_from, date_picker_to, indicator_choice.value))

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().clear()

curdoc().add_root(layout)