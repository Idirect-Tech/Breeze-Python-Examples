#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# *********************************************************************************************************************************************************************



# Import Libraries

from datetime import datetime
import pandas as pd
from breeze_connect import BreezeConnect

# Setup my API keys 
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)


# *********************************************************************************************************************************************************************

# Callback to receive ticks.
# Event based function

def on_ticks(ticks):
    data.append(ticks)
    if(len(data) > 10): close()
    
def close():
  api.ws_disconnect()
  df = pd.DataFrame(data)
  df.to_csv('data.csv')
        
# *********************************************************************************************************************************************************************
    
  
# Main Function        
if __name__ == "__main__":
    print ("Starting Execution \n")

    # List to store tick data
    data=[]

    #Switch on Websockets
    api.ws_connect()
    api.on_ticks = on_ticks
    
    api.subscribe_feeds(exchange_code="NFO", 
                    stock_code='NIFTY', 
                    product_type="options", 
                    expiry_date='27-Apr-2023', 
                    strike_price='17500', 
                    right='call', 
                    get_exchange_quotes=True, get_market_depth=False)
    
