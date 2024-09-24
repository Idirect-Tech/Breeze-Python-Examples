import pandas as pd 
import numpy as np 
from breeze_connect import BreezeConnect
import backtrader as bt
from datetime import datetime
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

file = open("config.txt", "r")
keys = file.read().split(",")

key_api = keys[0]
key_secret = keys[1]
key_session = keys[2]


breeze = BreezeConnect(api_key=key_api)
breeze.generate_session(api_secret=key_secret, session_token=key_session)

class RSIStrategy(bt.Strategy):
    params = (
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30)
    )

    def __init__(self):
        self. rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def next(self):
        if self.rsi < self.params.rsi_oversold:
            self.buy()
            # self.place_buy_order()

        elif self.rsi > self.params.rsi_overbought:
            self.sell()
            # self.place_sell_order()

    # def place_buy_order(self):
    #     breeze.place_order(stock_code="ITC",
    #                 exchange_code="NSE",
    #                 product="cash",
    #                 action="buy",
    #                 order_type="market",
    #                 stoploss="",
    #                 quantity="1",
    #                 price="",
    #                 validity="day"
    #             )

    # def place_sell_order(self):

    #     breeze.place_order(stock_code="ITC",
    #                 exchange_code="NSE",
    #                 product="cash",
    #                 action="sell",
    #                 order_type="market",
    #                 stoploss="",
    #                 quantity="1",
    #                 price="",
    #                 validity="day"
    #             )

class CustomPandasData(bt.feeds.PandasData):
    params = (('datetime','datetime'),
            ('open', 'open'),
            ('high', 'high'),
            ('low', 'low'),
            ('close', 'close'),
            ('volume', 'volume')
            )


def datetime_to_iso(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'

def datetime_converter(dt_string):
    return pd.to_datetime(dt_string)


if __name__ == "__main__":
    current_time = datetime.now()
    to_date = datetime_to_iso(current_time)

    data_df = breeze.get_historical_data_v2(interval="5minute",
                            from_date= "2023-08-15T07:00:00.000Z",
                            to_date= to_date,
                            stock_code="ITC",
                            exchange_code="NSE",
                            product_type="cash")["Success"]
    
    
    data_df = pd.DataFrame(data_df)

    data_df["datetime"] = data_df["datetime"].apply(datetime_converter)
    
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIStrategy)

    data_feed = CustomPandasData(dataname=data_df)
    cerebro.adddata(data_feed)

    #Set up broker account
    cerebro.broker = bt.brokers.BackBroker()
    cerebro.broker.set_cash(100000)


    # #Run the Backtest
    cerebro.run()
    cerebro.plot()


