#Import the library
from breeze_strategies import Strategies

#Configure the strategy using API Keys and set stoploss/takeprofit level.
api_key = "YOUR_APP_KEY"
api_secret = "YOUR_SECRET_KEY"
api_session = 'YOUR_SESSION_KEY'

#Configure the strategy using API Keys and set stoploss/takeprofit level.
obj = Strategies(app_key = api_key,
                 secret_key =api_secret,
                 api_session = api_session,
                 max_profit = "100",
                 max_loss = "-100")


#Execute the strategy
obj.straddle(strategy_type = "long",
             stock_code = "NIFTY",
             strike_price = "18700",
             quantity = "50",
             expiry_date = "2023-06-29T06:00:00.000Z")
#SquareOff existing positions and exit the strategy of straddle
obj.stop() 
