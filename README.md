# Stock Analysis Web App

## Screenshot

![App Screenshot](https://drive.google.com/uc?export=view&id=1qhPPXoG8L1fQXxraUFgd1UoFp4CyU4uE)


## Overview

This project is a stock analysis web application built using Bokeh. It allows users to compare historical stock data of two different stocks, visualize price movements, and apply technical indicators such as moving averages and linear regression.

## Features
- Fetches historical stock data using the Twelve Data API.
- Supports two stock tickers for comparison.
- Allows selection of technical indicators:
  - 30-Day Simple Moving Average (SMA)
  - 100-Day Simple Moving Average (SMA)
  - Linear Regression Line
- Interactive candlestick chart with zoom and pan controls.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python packages (see below)

## Installation

Clone the repository and navigate into the project directory:

```sh
git clone YOUR_REPO_URL
cd YOUR_PROJECT_DIRECTORY
```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root and add your Twelve Data API key:

```ini
TWELVE_API_KEY=your_api_key_here
```

## Running the Web App

Start the Bokeh server:

```sh
bokeh serve --show your_script.py
```

Replace `your_script.py` with the actual filename of your Bokeh application script.

## Usage

1. Enter two stock ticker symbols.
2. Select a start and end date for data retrieval.
3. Choose technical indicators to display.
4. Click "Load Data" to fetch and visualize stock prices.


