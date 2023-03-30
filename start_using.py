#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# Select Stock (USE SYMBOL AS SHOWN ON NSE) eg: RELIANCE
STOCK = 'RELIANCE' 

# Import Libraries
from pip._internal import main as pipmain
pipmain(['install', 'breeze_connect'])
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)

STOCK = api.get_names('NSE', STOCK)['isec_stock_code']

api.place_order(stock_code=STOCK,
                exchange_code="NSE",product="cash",action="buy",
                order_type="market",stoploss="",quantity="1",price="",validity="day")
