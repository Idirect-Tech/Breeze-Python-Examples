# code used in [How to get started with Breeze API](https://www.youtube.com/watch?v=GtqrSDpj0NE)
from breeze_connect import BreezeConnect
import pandas as pd

app_key = ""
secret_key = ""
session_token = ""

# Initialize SDK
breeze = BreezeConnect(api_key=app_key)

# Generate Session
breeze.generate_session(api_secret=secret_key,
                        session_token=session_token)


hdata = breeze.get_historical_data_v2(interval="1minute",
                            from_date= "2022-08-15T07:00:00.000Z",
                            to_date= "2022-08-17T07:00:00.000Z",
                            stock_code="ICIBAN",
                            exchange_code="NFO",
                            product_type="futures",
                            expiry_date="2022-08-25T07:00:00.000Z",
                            right="others",
                            strike_price="0")

df_hdata = pd.DataFrame(hdata['Success'])
