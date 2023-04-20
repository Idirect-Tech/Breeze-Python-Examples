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


# Function to place order
def place_order(each_leg):

    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z')    
  
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
        
    else : 
        print('\nFailed to place order!\n', buy_order['Error'])


    
if __name__ == "__main__":
    print ("Starting Execution \n")
        
    # enter contract details
    cx = {'stock': 'NIFTY',
         'strike': '17750',
         'expiry': '2023-04-20T06:00:00.000Z',      
         'right': 'call',         
         'action': 'buy'}
    
    # Place order
    place_order(cx)
