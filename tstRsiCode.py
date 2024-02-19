import plotly.express as px 
from printTick import printTick
import matplotlib.pyplot as plt
import numpy as np
from tickerTester import tickerTester
import yfinance as yf
from procRes import procRes
import pandas as pd
import pandas_ta as ta


# key = 'bbmd'
key = 'rsimd'
tkr = 'ugi'
days = 365
datInterval = '1d'
pyd = 3
tFrame = '1y'
off = False


pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)  
pd.set_option('display.expand_frame_repr', False)


dat = yf.Ticker(tkr)
dInfo = dat.info #Ticker info
# print(dInfo)
df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

# Calculate the price change for each period
delta = df['Close'].diff()

# Define the period for the rolling average
period = 14

# Calculate the average gain and average loss for the specified period
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(period).mean()
avg_loss = loss.rolling(period).mean()

# Calculate the Relative Strength (RS) by dividing the average gain by the average loss
rs = avg_gain / avg_loss

# Calculate the Relative Strength Index (RSI)
rsi = 100 - (100 / (1 + rs))

# Add the RSI to the dataframe
df['RSI'] = rsi
print(df)