#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# *********************************************************************************************************************************************************************

# Import Libraries

from datetime import datetime
import time
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)

# **************************************************************************************************************        

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


# ******************************************************************************************************************************            

# Function to create a stoploss order at limit price
def add_sl(each_leg, price):
    
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
    action = 'buy' if each_leg['action'] == 'sell' else 'sell'
    print(f"\nSL for {each_leg['name']} added at {price}")
    
    try:
        # Place square off order 
        sq_off_order = api.square_off(exchange_code="NFO",
                    product="options",
                    stock_code=each_leg['stock'],
                    expiry_date=each_leg['expiry'],
                    right=each_leg['right'],
                    strike_price=each_leg['strike'],
                    action=action,
                    order_type="limit",
                    validity="day",
                    stoploss=str(price),
                    quantity="50",
                    price=str(price),
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

# Function to modify an existing stoploss order at new limit price
def modify_sl(order_id, price):
    
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
    print(f"Modifying Order {order_id} at market")
    
    try:
        # Place square off order 
        modify_order = api.modify_order(order_id=order_id,
                    exchange_code="NFO",
                    order_type="limit",
                    stoploss=str(price),
                    quantity="50",
                    price=str(price),
                    validity="day",
                    disclosed_quantity="0",
                    validity_date=today)

                
        if(modify_order['Status']==200) : 
            print(modify_order['Success'])

        else : 
            print('\nFailed to modify order!\n', modify_order)
            return False

    except Exception as error:
        print('Modify Order API Error!', error)
        return False
    
    
# ******************************************************************************************************************************                

# Function to fetch price at which order got executed
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
        
        
if __name__ == "__main__":
    print ("Starting Execution \n")
    
    #place order and store id
    cx = get_contract('NIFTY-17500-20/Apr/2023-CE', 'buy')
    order_id = place_order(cx)    
    
    time.sleep(1)
    # calculate price at which order got executed
    cost = get_cost(order_id)

    # enter stoploss percentage & calculate stoploss price (limit price for cover order)
    sl_percent = 20
    stoploss = round(cost * (1-sl_percent/100),1)

    time.sleep(1)
    # place the stoploss order / cover order at limit price
    stoploss_order = add_sl(cx, stoploss)
            
