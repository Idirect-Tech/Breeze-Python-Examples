#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# Select Stock (USE SYMBOL AS SHOWN ON NSE) eg: RELIANCE
STOCK = 'RELIANCE' 

import sys, subprocess, pkg_resources
module=True

def install():
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', 'breeze_connect'], stdout=subprocess.DEVNULL)
    print('Successfully installed Breeze !!')

while(module):
    try:
        from breeze_connect import BreezeConnect
        module=False
    except ModuleNotFoundError:
        print("module 'breeze_connect' is not installed. Installing it now...")    
        install()

try:
    # Connecting to demat account 
    api = BreezeConnect(api_key=api_key)
    api.generate_session(api_secret=api_secret,session_token=api_session)
    print("Successfully connected to demat account !!")    
    
except NameError:
    print("Connection to demat account failed !!")
    
try:
    STOCK = api.get_names('NSE', STOCK)['isec_stock_code']
    order = api.place_order(stock_code=STOCK,exchange_code="NSE",product="cash",action="buy",order_type="market",stoploss="",quantity="1",price="",validity="day")
    
    if(order['Status'] == 200):
        print(order['Success']['message'])
    else:
        print(order['Error'])
            
except Exception as e:
    print("API request failed. Please try again !!/n", e)
