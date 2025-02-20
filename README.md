# Financial Dashboard with Bokeh and Twelve Data API

This project is a financial dashboard that visualizes stock data using the Bokeh library and fetches historical stock data from the Twelve Data API. It allows users to compare two stocks, apply technical indicators, and view the data in an interactive chart.

## Features

- Fetch historical stock data for two tickers.
- Visualize stock data using candlestick charts.
- Apply technical indicators such as:
  - 30-Day Simple Moving Average (SMA)
  - 100-Day Simple Moving Average (SMA)
  - Linear Regression Line
- Interactive and responsive charts using Bokeh.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries:
  ```bash
  pip install bokeh pandas numpy requests python-dotenv
