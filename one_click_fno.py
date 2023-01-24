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
                        
  
# Connect to websocket
api.ws_connect()

# Callback to receive ticks
def on_ticks(ticks):
    print("Ticks: {}".format(ticks))

api.on_ticks = on_ticks

api.subscribe_feeds(stock_token = "one_click_fno")
