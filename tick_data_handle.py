#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

#make sure to install latest library of Breeze using --> pip install --upgrade breeze-connect 

import time
import pandas as pd
from datetime import timedelta, datetime

from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key=api_key)

# Generate Session
breeze.generate_session(api_secret=api_secret,
                        session_token=api_session)
                        
  
# Connect to websocket
api.ws_connect()

#list to store tick data message
tick_feed = []

# Callback to receive ticks
def on_ticks(ticks):
    tick_feed.append(ticks)
#     print("Ticks: {}".format(ticks))

api.on_ticks = on_ticks

api.subscribe_feeds(exchange_code="NFO", 
                               stock_code="NIFTY", 
                               product_type="options", 
                               expiry_date="25-Jan-2023", 
                               strike_price="18000", right="Call", interval="1second")


#wait for 30 seconds (enough time to collect some data in tick_feed list)
time.sleep(30)

#convert list of dict into dataframe
data = pd.DataFrame(tick_feed)
print(data)
