#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
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
                'expiry_date':expiry.strftime('%d-%m-%Y'),
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
                                    stoploss='',
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
    print(f"\nSquaring off {each_leg['name']} at market")
    
    try:
        # Place square off order 
        sq_off_order = api.square_off(exchange_code="NFO",
                    product="options",
                    stock_code=each_leg['stock'],
                    expiry_date=each_leg['expiry'],
                    right=each_leg['right'],
                    strike_price=each_leg['strike'],
                    action="sell",
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
            print(sq_off_order)
            return order_id

        else : 
            print('\nFailed to square off!\n', sq_off_order['Error'])
            return False

    except Exception as error:
        print('Place Order API Error!', error)
        return False

# **************************************************************************************************************            

    
if __name__ == "__main__":
    print ("Starting Execution \n")
        
    # Create Basket
    cx1 = get_contract('NIFTY-17600-27/apr/2023-CE', 'buy')
    cx2 = get_contract('NIFTY-17700-27/apr/2023-CE', 'buy')
    cx3 = get_contract('NIFTY-17650-27/apr/2023-CE', 'sell')

    basket = []
    basket.extend([cx1,cx2,cx3,cx3)
                   
    # Place order
    for cx in basket:
      order_id = place_order(cx,'market')
      print(order_id)
