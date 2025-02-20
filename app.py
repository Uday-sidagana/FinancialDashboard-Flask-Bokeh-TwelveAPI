import math
import numpy as np
import datetime as dt

import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Button, TextInput, DatePicker, MultiChoice
from bokeh.layouts import column, row

import time

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")
print(f"Your API Key: {api_key}")  # Optional: for testing purposes


def load_data(ticker1, ticker2, start, end): 
    # Ticker = Financial abbreviation ex. Axiom is abbreviated as XOM
    df1= yf.download(ticker1, start, end)
    
    time.sleep(5)
    df2 = yf.download(ticker2, start, end)

    if df1.empty or df2.empty:
        print("Error: No data retrieved for one or both tickers")
        return None, None

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
    p.line(df.index, y_predicted, legend_label="Linear Regression", color="red")


    p.vbar(df.index[gain].values, width, df.Open[gain].values, df.Close[gain].values, fill_color="#00ff00", line_color="00ff00")
    p.vbar(df.index[loss].values, width, df.Open[loss].values, df.Close[loss].values, fill_color="#ff0000", line_color="ff0000")



    for indicator in indicators:
        if indicator == "30 Day SMA":
            df["SMA30"] = df["Close"].rolling(30).mean()
            p.line(df.index, df.SMA30, color ="purple", legend_label="30 DAY SMA")

        elif indicator == "100 Day SMA":
            df["SMA100"] = df["Close"].rolling(100).mean()
            p.line(df.index, df.SMA100, color="purple", legend_label="100 DAY SMA")

        elif indicator == "Linear Regression Line":
            par = np.polyfit(range(len(df.index.values)), df.Close.values, 1, full=True)
            slope = par[0][0]
            intercept = par[0][1]
            y_predicted = [slope * i + intercept for i in range(len(df.index.values))]
            p.segment(df.index[0], y_predicted[0], df.index[-1], y_predicted[-1], legend_label="Linear Regression",
                      color="red")
            #chatgpt end
    
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    return p



def on_button_click(ticker1, ticker2, start, end, indicators):
    df1, df2 = load_data(ticker1, ticker2, start, end)
    p1= plot_data(df1, indicators)
    p2= plot_data(df2, indicators, sync_axis=p1.x_range)
    
    curdoc().clear()
    curdoc().add_root(column(layout, row(p1, p2)))


#UI LAYOUT(Choosing start date, end, Text, Labels, indicators and buttons)

stock1_text = TextInput(title = "Stock 1")
stock2_text = TextInput(title = "Stock 2")

date_picker_from = DatePicker(title = "Start Date", value ="2025-01-01", min_date='2000-01-01', 
                              max_date=dt.datetime.now().strftime("%Y-%m-%d"))

date_picker_to = DatePicker(title = "End Date", value ="2025-02-01", min_date='2000-01-01', 
                            max_date=dt.datetime.now().strftime("%Y-%m-%d"))

indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"])

load_button = Button(label = "Load Data", button_type ='success')

load_button.on_click(lambda :on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, indicator_choice.value))

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)


curdoc().clear()
curdoc().add_root(layout)