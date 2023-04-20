#intialize keys

api_key = "INSERT_YOUR _APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# Import Libraries

from datetime import datetime
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)


# **************************************************************************************************************        

# Function to generate a signal
def place_order(each_leg):

    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    

    # Place options order 
    buy_order = api.place_order(stock_code=each_leg['stock'],
                                exchange_code="NFO",
                                product="options",
                                action=each_leg['action'],
                                order_type='market',
                                stoploss="",
                                quantity="50",
                                price="",
                                validity="day",
                                validity_date=today,
                                disclosed_quantity="0",
                                expiry_date=each_leg['expiry'],
                                right=each_leg['right'],
                                strike_price=each_leg['strike'])

    if(buy_order['Status']==200) : 
        order_id = buy_order['Success']['order_id']
        print(f'Successfully placed market order !\nOrder ID is {order_id}')

    else : 
        print('\nFailed to place order!\n', buy_order['Error'])

# **************************************************************************************************************        

def square_off_at_market(each_leg):
    
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
    # Place square off order 
    sq_off_order = api.square_off(exchange_code="NFO",
                product="options",
                stock_code=each_leg['stock'],
                expiry_date=each_leg['expiry'],
                right=each_leg['right'],
                strike_price=each_leg['strike'],
                action='sell',
                order_type="market",
                validity="day",
                stoploss="",
                quantity="50",
                price="0",
                validity_date=today,
                trade_password="",
                disclosed_quantity="0")


    if(sq_off_order['Status']==200) : 
        print(sq_off_order)

    else : 
        print('\nFailed to square off!\n', sq_off_order['Error'])
        return False

# ******************************************************************************************************************************            

# Callback to receive ticks.
# Event based function

def on_ticks(ticks):    

    ltp = ticks['last']        
    print(f"LTP : {round(ltp,1)} | Level : {round(level,1)} | , SL : {round(trailing_stoploss,1)}")

    # increase cost and SL if price level crosses threshold
    if(ltp > level*1.05):      
        print(">>>>  revising SL  <<<<<")
        level = ltp
        trailing_stoploss = level*0.95

    # Square off if price level falls below trailing SL
    if(ltp < trailing_stoploss):
        #square off now
        print(">>>>  ALERT : square off now  <<<<<")
        square_off_at_market(cx)


if __name__ == "__main__":
    print ("Starting Execution \n")
    
    # Start streaming service i.e Websockets
    api.ws_connect()
    api.on_ticks = on_ticks
    
    # Select Contract
    cx = {'stock': 'NIFTY',
         'strike': '17750',
         'expiry': '2023-04-20T06:00:00.000Z',      
         'right': 'call',         
         'action': 'buy'}
    
    # Place order
    place_order(cx)

    #Initialize variables 
    cost, level, take_profit, trailing_stoploss = 0,0,0,0
    
    # Wait for few seconds for order to get successfully executed    
    time.sleep(2)
    
    # Get the execution price    
    detail = api.get_order_detail('nfo',order_id)
    cost = float(detail['Success'][0]['average_price'])
    trailing_stoploss = round(cost * 0.95,1)

    print(f"Entry Cost : {cost}")
    print(f"Setting SL : {trailing_stoploss}")
    
    #subscribe to feeds
    api.subscribe_feeds(exchange_code="NFO", 
                    stock_code='NIFTY', 
                    product_type="options", 
                    expiry_date='20-Apr-2023', 
                    strike_price='17750', 
                    right='call', 
                    get_exchange_quotes=True, get_market_depth=False)
