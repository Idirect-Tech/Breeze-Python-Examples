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

# Function to create a contract

def get_contract(name, action):
    name = name.upper()
    details = name.split('-')
    details[-1] = 'call' if (details[-1] == 'CE') else 'put'
    
    if (details[2].split("/")[1] in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']):
        expiry = datetime.strptime(details[2], "%d/%b/%Y")
    else :
        expiry = datetime.strptime(details[2], "%d/%m/%Y")
                
    contract = {'stock':details[0],
                'strike': details[1],
                'expiry': expiry.strftime('%Y-%m-%dT06:00:00.000Z'),
                'expiry_date':expiry.strftime('%d-%b-%Y'),
                'right': details[-1],
                'name': name,
                'action' : action
    }
    
    return contract

# **************************************************************************************************************        

# Function to generate a signal
def place_order(each_leg):

    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
    print(f"\nPlacing {each_leg['right']} {each_leg['action']} market order")

    try:
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
            return order_id

        else : 
            print('\nFailed to place order!\n', buy_order['Error'])
            return False

    except Exception as error:
        print('Place Order API Error!', error)
        return False

# **************************************************************************************************************        

def square_off_at_market(each_leg):
    
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
    action = 'buy' if each_leg['action'] == 'sell' else 'sell'
    print(f"\nSquaring off {each_leg['name']} at market")
    
    try:
        # Place square off order 
        sq_off_order = api.square_off(exchange_code="NFO",
                    product="options",
                    stock_code=each_leg['stock'],
                    expiry_date=each_leg['expiry'],
                    right=each_leg['right'],
                    strike_price=each_leg['strike'],
                    action=action,
                    order_type="market",
                    validity="day",
                    stoploss="",
                    quantity="50",
                    price="0",
                    validity_date=today,
                    trade_password="",
                    disclosed_quantity="0")

                
        if(sq_off_order['Status']==200) : 
            order_id = sq_off_order['Success']['order_id']
            msg = sq_off_order['Success']['message']
            print(f"{msg} : {order_id}")
            return order_id


        else : 
            print('\nFailed to square off!\n', sq_off_order['Error'])
            return False

    except Exception as error:
        print('Place Order API Error!', error)
        return False

# ******************************************************************************************************************************            

# Callback to receive ticks.
# Event based function

def on_ticks(ticks):    
    global level, trailing_stoploss

    #trailing StopLoss
    if ('last' in ticks.keys()):
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
            close()
                       
api.on_ticks = on_ticks
# ******************************************************************************************************************************            

#Switch on Websockets
def socket():
    api.ws_connect()
    api.on_ticks = on_ticks
    
    
# ******************************************************************************************************************************                

# This function checks the order status and returns the execution price 
def get_cost(order_id):
    try:
        detail = api.get_order_detail('nfo',order_id)
        if(detail['Status']==200):
            
            cost = float(detail['Success'][0]['average_price'])
            status = detail['Success'][0]['status']
            print(f"Order Status : {status}")
            return cost
        else:
            print(detail)
    except:
        print('API Failed !!')
    

# ******************************************************************************************************************************            

# This function squares off open position and stops the streaming. Algo will stop after this.
def close():
    
    api.ws_disconnect()
    print(">>>>  Squaring off now  <<<<<")
    square_off_at_market(cx)
    
    
# ******************************************************************************************************************************            


if __name__ == "__main__":
    print ("Starting Execution \n")
    
    # Start streaming service i.e Websockets
    socket() 
    
    # Select Contract
    cx = get_contract('NIFTY-17750-20/Apr/2023-CE', 'buy')
    
    # Place order
    order_id = place_order(cx)

    #Initialize variables 
    cost, level, take_profit, trailing_stoploss = 0,0,0,0
    
    # Wait for few seconds for order to get successfully executed    
    time.sleep(2)
    
    # Get the execution price    
    cost = get_cost(order_id)
    level = cost
    take_profit = round(cost*1.1,1)
    trailing_stoploss = round(cost * 0.95,1)

    print(f"Entry Cost : {cost}")
    print(f"Setting SL : {trailing_stoploss}")
    print(f"Setting TP : {take_profit}")
    
    #subscribe to feeds
    api.subscribe_feeds(exchange_code="NFO", 
                    stock_code=cx['stock'], 
                    product_type="options", 
                    expiry_date=cx['expiry_date'], 
                    strike_price=cx['strike'], 
                    right=cx['right'], 
                    get_exchange_quotes=True, get_market_depth=False)
