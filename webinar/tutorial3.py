# code used in [Researching trading strategies using Pandas framework](https://www.youtube.com/watch?v=I4BAUYUyr7Q)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_hdata = pd.read_csv('/home/builder/Downloads/ICICIBANK_HistoricalData.csv')
df_hdata.shape
df_hdata.columns
df_hdata.head(10)
df_hdata.tail()

df_close = df_hdata[['datetime', 'close']].copy()
df_close.shape
df_close.columns
df_close.head()
df_close.tail()
df_close['close'].max()
df_close['close'].min()

#let's take a look at the chart, how does it look, get a feel for it
df_close['close'].plot(fontsize = 12)
plt.grid()
plt.ylabel('Price in Rupees')
plt.show()

# Create 20 days simple moving average column
df_close['20_SMA'] = df_close['close'].rolling(window = 20, min_periods = 20).mean()
# Create 50 days simple moving average column
df_close['50_SMA'] = df_close['close'].rolling(window = 50, min_periods = 50).mean()
# take a peep
df_close.head(25)
df_close.tail()

# plot short and long moving averages 
plt.figure(figsize = (20, 10))
#ultratech_df['Close Price'].plot(color = 'k', lw = 1)
df_close['close'].plot(color = 'r', lw = 1)
df_close['20_SMA'].plot(color = 'b', lw = 1)
df_close['50_SMA'].plot(color = 'g', lw = 1)
plt.grid()
plt.show()

# generate signals
df_close['Signal'] = 0.0  
df_close['Signal'] = np.where(df_close['20_SMA'] > df_close['50_SMA'], 1.0, 0.0) 


# create a new column 'Position' which is a day-to-day difference of the 'Signal' column. 
df_close['Position'] = df_close['Signal'].diff()

# display the dataframe
df_close.tail(10)

# visualize the strategy as it would play out
plt.figure(figsize = (20,10))
plt.tick_params(axis = 'both', labelsize = 14)
# plot close price, short-term and long-term moving averages 
df_close['close'].plot(color = 'k', lw = 1, label = 'Close Price')  
df_close['20_SMA'].plot(color = 'b', lw = 1, label = '20-day SMA') 
df_close['50_SMA'].plot(color = 'g', lw = 1, label = '50-day SMA') 

# plot 'buy' signals
plt.plot(df_close[df_close['Position'] == 1].index, 
         df_close['20_SMA'][df_close['Position'] == 1], 
         '^', markersize = 15, color = 'g', alpha = 0.7, label = 'buy')

# plot 'sell' signals 
plt.plot(df_close[df_close['Position'] == -1].index, 
         df_close['20_SMA'][df_close['Position'] == -1], 
         'v', markersize = 15, color = 'r', alpha = 0.7, label = 'sell')
plt.ylabel('Price in Rupees', fontsize = 15 )
plt.xlabel('Date', fontsize = 15 )
plt.title('ICICIBANK - SMA Crossover chart', fontsize = 20)
plt.legend()
plt.grid()
plt.show()

df_close.to_csv('/home/builder/Downloads/ICICIBANK_SMA20-50_Strategy.csv')
