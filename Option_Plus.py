# Make sure to install latest library of Breeze before trying the below code. 
# shell command => pip install --upgrade breeze-connect 


#intialize keys
api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

#import libraries
from breeze_connect import BreezeConnect

# Initialize SDK
api = BreezeConnect(api_key=api_key)

# Generate Session
api.generate_session(api_secret=api_secret,
                      session_token=api_session)


# Place Option Plus order. 
# Below code will place 2 orders - fresh order and cover SLTP order.
# Cover SLTP order is the limit order which squares off your fresh order at limit price when the price hits stop loss trigger price.

option_plus_order = api.place_order(stock_code="NIFTY",
                                   exchange_code="NFO",
                                   product="optionplus",
                                   action="buy",
                                   order_type="limit",
                                   quantity="50",
                                   price="0.05", #limit price
                                   stoploss='1', # SLTP
                                   validity="day",
                                   disclosed_quantity="0",
                                   validity_date="2023-03-20T06:00:00.000Z",
                                   expiry_date="2023-03-23T06:00:00.000Z",
                                   right="call",
                                   strike_price="17500",
                                   order_type_fresh="limit",
                                   order_rate_fresh="2", # fresh order price. 
                                   user_remark="Test")


fresh_order_id = float(option_plus_order["Success"]["order_id"])
cover_order_id = fresh_order_id + 1

print(" Order ID :",id)

# To square off option plus order :
# In Opiton Plus order, to square off your position - simply convert cover order from limit to market. 

modify_order = api.modify_order(order_id=str(cover_order_id),
                    exchange_code="NFO",
                    order_type="market",
                    stoploss="",
                    quantity="50",
                    price="",
                    validity="day",
                    disclosed_quantity="0",
                    validity_date="2023-03-20T06:00:00.000Z")


print(modify_order)
