import math
import numpy as np
import datetime as dt
import pandas as pd
import requests

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Button, TextInput, DatePicker, MultiChoice
from bokeh.layouts import column, row

from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("TWELVE_API_KEY")


def load_data(ticker1, ticker2, start, end):
    """
    Fetch historical stock data from Twelve Data API.
    """
    base_url = "https://api.twelvedata.com/time_series"

    def fetch_data(ticker):
        params = {
            "symbol": ticker,
            "interval": "1day",
            "start_date": start,
            "end_date": end,
            "apikey": api_key,
            "outputsize": "5000"
        }
        response = requests.get(base_url, params=params).json()

        if "values" not in response:
            print(f"Error fetching data for {ticker}: {response.get('message', 'Unknown error')}")
            return None

        df = pd.DataFrame(response["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.set_index("datetime", inplace=True)

        df = df.astype(float)  # Convert all numeric columns
        return df

    df1 = fetch_data(ticker1)
    df2 = fetch_data(ticker2)

    if df1 is None or df2 is None:
        return None, None

    return df1, df2


def plot_data(data, indicators, sync_axis=None):
    """
    Plots stock data with selected indicators.
    """
    df = data
    gain = df.close > df.open
    loss = df.close < df.open
    width = 12 * 60 * 60 * 1000  # Candle width (milliseconds)

    p = figure(
        tools="pan, wheel_zoom, box_zoom, reset, save",
        x_axis_type="datetime", width=1000, x_range=sync_axis if sync_axis else None
    )

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25

    p.vbar(df.index[gain], width, df.open[gain], df.close[gain], fill_color="#00ff00", line_color="00ff00")
    p.vbar(df.index[loss], width, df.open[loss], df.close[loss], fill_color="#ff0000", line_color="ff0000")

    # Indicator calculations
    y_predicted = None

    for indicator in indicators:
        if indicator == "30 Day SMA":
            df["SMA30"] = df["close"].rolling(30).mean()
            p.line(df.index, df.SMA30, color="purple", legend_label="30 DAY SMA")

        elif indicator == "100 Day SMA":
            df["SMA100"] = df["close"].rolling(100).mean()
            p.line(df.index, df.SMA100, color="blue", legend_label="100 DAY SMA")

        elif indicator == "Linear Regression Line":
            x_values = np.arange(len(data.index))
            slope, intercept = np.polyfit(x_values, data["close"].values, 1)
            y_predicted = slope * x_values + intercept

    # Plot linear regression if calculated
    if y_predicted is not None:
        p.line(data.index, y_predicted, legend_label="Linear Regression", color="red")

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    return p


def on_button_click():
    """
    Handles button click to load data and update the plot.
    """
    ticker1 = stock1_text.value.strip()
    ticker2 = stock2_text.value.strip()
    start = date_picker_from.value
    end = date_picker_to.value
    indicators = indicator_choice.value

    df1, df2 = load_data(ticker1, ticker2, start, end)

    if df1 is None and df2 is None:
        print("Error: No data retrieved.")
        return

    p1 = plot_data(df1, indicators)
    p2 = plot_data(df2, indicators, sync_axis=p1.x_range)

    curdoc().clear()
    curdoc().add_root(column(layout, row(p1, p2) if p1 and p2 else row(p1 or p2)))


# UI Elements
stock1_text = TextInput(title="Stock 1")
stock2_text = TextInput(title="Stock 2")

date_picker_from = DatePicker(
    title="Start Date", value="2025-01-01",
    min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d")
)

date_picker_to = DatePicker(
    title="End Date", value="2025-02-01",
    min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d")
)

indicator_choice = MultiChoice(
    title="Select Indicators",
    options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"]
)

load_button = Button(label="Load Data", button_type="success")
load_button.on_click(on_button_click)

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().clear()
curdoc().add_root(layout)
