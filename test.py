import yfinance as yf

ticker1 = "NVR"
ticker2 = "SEB"
start = "2024-01-01"
end = "2025-02-20"


df1 = yf.download(ticker1, start, end)
import time    
time.sleep(5)


df2 = yf.download(ticker2, start, end)

print(df1.head())
print(df2.head())
