#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'



# Define Contract
stock = 'NIFTY',
strike = '17750',
expiry = '2023-04-20T06:00:00.000Z',      
right = 'call',         




# Import Libraries

from datetime import datetime
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)

# Place order
buy_order = api.place_order(stock_code=stock,
                            exchange_code="NFO",
                            product="options",
                            action='buy',
                            order_type='market',
                            stoploss="",
                            quantity="50",
                            price="",
                            validity="day",
                            validity_date=today,
                            disclosed_quantity="0",
                            expiry_date=expiry,
                            right=right,
                            strike_price=strike)

print(buy_order)
