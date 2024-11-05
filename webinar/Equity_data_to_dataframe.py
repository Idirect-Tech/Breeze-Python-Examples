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


# Fetch Data using historical data API v2
data = api.get_historical_data_v2(interval="1minute",
                            from_date= "2022-08-15T07:00:00.000Z",
                            to_date= "2022-08-17T07:00:00.000Z",
                            stock_code="ITC",
                            exchange_code="NSE",
                            product_type="cash")


# Convert data (API JSON response) into a table / dataframe using pandas library
import pandas as pd
df = pd.DataFrame(data['Success'])

print(df)
