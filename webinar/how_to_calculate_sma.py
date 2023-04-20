### Enter your API Keys
api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

import time
import pandas as pd
from datetime import timedelta, datetime

from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key=api_key)

# Generate Session
breeze.generate_session(api_secret=api_secret,
                        session_token=api_session)

# initialize user inputs


def get_sma():
    STOCK = "BHEL"
    current_time = datetime.now()
    from_date = current_time - timedelta(days=20)
    
    # note that we have converted dates to ISO time-format before making API call
    data = breeze.get_historical_data_v2(interval='1day',
                                        from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                        to_date = current_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                        stock_code=STOCK,
                                        exchange_code="NSE",
                                        product_type="cash")


    # Calculate simple moving average of 'close' price
    data = pd.DataFrame(data['Success'])
    data.close = data.close.astype(float)
    sma = round(data.close.mean(),2)
    return sma
        
if __name__ == "__main__":
    indicator = get_sma()
    print(indicator)
