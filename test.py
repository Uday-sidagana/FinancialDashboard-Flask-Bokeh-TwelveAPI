import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("API_KEY")

def load_data(ticker1, ticker2, start, end):
    ts = TimeSeries(key=api_key, output_format='pandas')

    df1, _ = ts.get_daily(symbol=ticker1, outputsize="full")
    df2, _ = ts.get_daily(symbol=ticker2, outputsize="full")

    # Rename columns to standard format
    df1.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"}, inplace=True)
    df2.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"}, inplace=True)

    df1.index = pd.to_datetime(df1.index)
    df2.index = pd.to_datetime(df2.index)

    df1 = df1[start:end]
    df2 = df2[start:end]

    if df1.empty or df2.empty:
        print("Error: No data retrieved for one or both tickers")
        return None, None

    return df1, df2

# Test Parameters
ticker1 = "AAPL"
ticker2 = "GOOGL"
start = "2025-01-01"
end = "2025-02-01"

# Run Test
df1, df2 = load_data(ticker1, ticker2, start, end)

if df1 is not None and df2 is not None:
    print("Data for", ticker1, ":\n", df1.head())
    print("\nData for", ticker2, ":\n", df2.head())
else:
    print("Failed to retrieve data.")
