import time
from breeze_connect import BreezeConnect
from datetime import datetime, timedelta
key_api = ""
key_secret = ""
key_session = ""
breeze = BreezeConnect(api_key=key_api)
breeze.generate_session(api_secret=key_secret, session_token=key_session)

# Connect to websocket(it will connect to tick-by-tick data server)
breeze.ws_connect()

# Callback to receive ticks.
def on_ticks(ticks):
    print("Ticks: {}".format(ticks))

# Assign the callbacks.
breeze.on_ticks = on_ticks


# Sample Code for Subscribing Live Feeds for Multiple Stocks:
 
breeze.get_names(exchange_code = 'NSE',stock_code = 'TATASTEEL')["isec_token_level1"]
 
# Output: "4.1!3499"
 
breeze.get_names(exchange_code = 'NSE',stock_code = 'RELIANCE')["isec_token_level1"]
 
# Output : "4.1!2885"

breeze.subscribe_feeds(stock_token=['4.1!3499','4.1!2885'])


# Stock token can be find out from below file also.

# https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv

