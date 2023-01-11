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

# Callback to receive ticks.
tick_feed = []
def on_ticks(ticks):
    tick_feed.append(ticks)
#     print("Ticks: {}".format(ticks))

api.on_ticks = on_ticks

