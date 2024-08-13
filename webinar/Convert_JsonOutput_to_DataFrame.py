
#import library
from breeze_connect import BreezeConnect

#Initiliaze SDK
breeze = BreezeConnect(api_key="xxxxx")

#Generate Session
breeze.generate_session(api_secret="xxxxxx",session_token="xxxxx")


#Use get_historical_data_v2 SDK to fetch historical data
df = breeze.get_historical_data_v2(interval="1second",
from_date= "2023-08-08T:40:00.000Z",
to_date= "2023-08-08T12:41:00.000Z",
stock_code="NIFTY",
exchange_code="NFO",
product_type="options",
expiry_date="2023-08-10T07:00:00.000Z",
right="put",
strike_price="19550")

#Parse data to dataframe
df = pd.DataFrame(df["Success"])

print(df)