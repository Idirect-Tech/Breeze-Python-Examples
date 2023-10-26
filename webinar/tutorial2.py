# code used in [Analysing historical market data from Breeze API using Pandas framework](https://www.youtube.com/watch?v=uZgAKrIMZBE)
from breeze_connect import BreezeConnect
from datetime import datetime
from datetime import timedelta

app_key = ""
secret_key = ""
session_token = ""

# Initialize SDK
breeze = BreezeConnect(api_key=app_key)

# Generate Session
breeze.generate_session(api_secret=secret_key,
                        session_token=session_token)

hdata = breeze.get_historical_data_v2(interval="1minute",
                            from_date= "2022-08-15T07:00:00.000Z",
                            to_date= "2022-08-17T07:00:00.000Z",
                            stock_code="ICIBAN",
                            exchange_code="NFO",
                            product_type="futures",
                            expiry_date="2022-08-25T07:00:00.000Z",
                            right="others",
                            strike_price="0")

# SUPER UTLITY - POWER TOOL
type(hdata)
hdata.keys()
type(hdata['Error'])
type(hdata['Status'])
type(hdata['Success'])

hdata['Error']==None
hdata['Status']
hdata['Success']

len(hdata['Success'])
hdata['Success'][0]
hdata['Success'][-1].keys()

list_dict_hdata = hdata['Success']

# getting Breeze historical data in a loop
dtm_from = datetime(2022, 1, 1, 0, 0, 0)
dtm_to   = datetime(2023, 1, 1, 0, 0, 0)

# set up some helping variables
tdelta_1day = timedelta(days=1)     # note that this can be cahnged to 7 if you want only a particular weekday, like expiries. will require modifications below
tdelta_days = dtm_to - dtm_from + tdelta_1day
list_dtm_dates = [dtm_from]

# for loop method
for i in range(tdelta_days.days):
    list_dtm_dates.append(list_dtm_dates[-1] + tdelta_1day)

# introducing list comprehension in python
list_dtm_dates = []
list_dtm_dates = [dtm_from + tdelta_1day*i for i in range(0, tdelta_days.days)]

# removing weekends
list_dtm_dates = [x for x in list_dtm_dates if x.weekday()<5]   # this step can also be used to isolate an expiry date

list_dtm_dates[0]
list_dtm_dates[-1]
len(list_dtm_dates)

# finding out how many days to request at a time given a candle size - note that constants are denoted by ALL CAPS variable names to differentiate from common variables that can be changed by the program itself
import math
int_candle_size = 5         # we want 5 minute candles
CANDLES_IN_A_DAY = 375      # NSE runs from 9:15 to 15:30, which means there are 45 + 5*60 + 30 = 375 minutes in 1 trading session on NSE
MAX_LINES = 1000            # Max number of historical candles that Breeze can send

int_max_days = math.floor(MAX_LINES/(CANDLES_IN_A_DAY/int_candle_size))
len(list_dtm_dates)/int_max_days

list_data = []

date_start = list_dtm_dates[0]
for i in range(int(len(list_dtm_dates)/int_max_days)):
    print(i)
    try:
        date_end = list_dtm_dates[int_max_days*(i+1)]
    except:
        date_end = list_dtm_dates[-1] + tdelta_1day
    print(date_start)
    print(date_end)
    list_dict_hdata = breeze.get_historical_data_v2(interval=str(int_candle_size)+"minute",
                            from_date= date_start.isoformat(),
                            to_date= date_end.isoformat(),
                            stock_code="ICIBAN",
                            exchange_code="NSE",
                            product_type="cash"
                            )["Success"]
    list_data = list_data + list_dict_hdata
    try:
        date_start = list_dtm_dates[list_dtm_dates.index(date_end)+1]
    except:
        pass

# LISTS
a = [1,2,3,4,5,6]
b = ['a', 'b', 'c']
a+b
b+a
a.append(b)

# DICTIONARIES
a = {'ltp': 100, 'ltq': 20, 'oi': 10000}
a.keys()
a.values()

a['ltp']
a.get('ltq')

a('close')

if a.get('close')==None:
    a['close'] = 200

# pip install pandas
import pandas as pd

# basic time series in Pandas - with explanation of descriptive, diagnostic, predictive, prescriptive analytics
a = {'a': 1, 'b':2, 'c': 3}
series_a = pd.Series(a.values(), a.keys())
series_a['a']
series_a.get('a')
series_a.get(0)
series_a.iloc[0]

# apply SMA in Pandas
df_hdata = pd.DataFrame(list_data)
df_hdata.shape
df_hdata.head()
df_hdata.head(10)
df_hdata.tail()
df_hdata.tail(10)
df_hdata['datetime'][0]
df_hdata['datetime'][17339]
df_hdata.columns
df_hdata.columns[0]
df_hdata.columns[-1]

# POWERTOOL ! export data to CSV or Excel format
df_hdata.to_csv('/home/builder/Downloads/ICICIBANK_HistoricalData.csv')
df_hdata.to_excel('/home/builder/Downloads/ICICIBANK_.xlsx')

type(df_hdata['close'])
dir(df_hdata['close'])


df_hdata['pandas_SMA_12'] = df_hdata['close'].rolling(window=12).mean()
df_hdata.head(13)

# visualize
import matplotlib.pyplot as plot
ts = pd.Series(data=df_hdata['pandas_SMA_12'], index=df_hdata['pandas_SMA_12'])
ts.plot()
plot.show()

df_hdata.plot(x='pandas_SMA_12', y='close')
plot.show()
df_hdata['pandas_SMA_12'].drop()

# backtest Moving Average Crossover in Pandas
# NEXT SESSION
