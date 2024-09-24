from breeze_connect import BreezeConnect
import pandas as pd 
from datetime import datetime, time as datetime_time
import time
import threading
import queue
import logging as logger
import warnings
warnings.filterwarnings('ignore')

file = open("config.txt", "r")
keys = file.read().split(",")

key_api = keys[0]
key_secret = keys[1]
key_session = keys[2]

logger.basicConfig(level=logger.INFO, handlers=[logger.StreamHandler()])

options_basket = [
    {"stock_code": "NIFTY", "expiry_date": "25-Jul-2024", "strike_price": "24950", "right": "Call"},
]

max_loss = 1000  
max_profit = 500
end_time = datetime_time(15, 30)
trailing_percentage = 10
quantity = 25

# Initialize BreezeConnect
breeze = BreezeConnect(api_key=key_api)
breeze.generate_session(api_secret=key_secret, session_token=key_session)

# Create a queue to store ticks
ticks_queue = queue.Queue()

last_price_tick = None
last_price_tick_lock = threading.Lock()

# Callback to receive ticks and put them in the queue
def on_ticks(ticks):
    ticks_queue.put(ticks)

# Assign the callbacks
breeze.on_ticks = on_ticks
breeze.subscribe_feeds(get_order_notification=True)
running = True

# Function to continuously process ticks and save them into a DataFrame
def process_ticks():
    global last_price_tick
    while running:
        ticks = []
        while not ticks_queue.empty():
            ticks.append(ticks_queue.get())
        if ticks:
            df = pd.DataFrame(ticks)
            latest_tick = df.iloc[-1].to_dict()
            with last_price_tick_lock:
                last_price_tick = latest_tick["last"]
            
# Start a separate thread for continuous processing
ticks_thread = threading.Thread(target=process_ticks, daemon=True)
ticks_thread.start()

# Connect to the websocket
breeze.ws_connect()

# Subscribe to feeds for each option in the basket
for option in options_basket:
    breeze.subscribe_feeds(exchange_code="NFO", 
                           stock_code=option["stock_code"], 
                           product_type="options", 
                           expiry_date=option["expiry_date"], 
                           strike_price=option["strike_price"], 
                           right=option["right"], 
                           get_exchange_quotes=True, 
                           get_market_depth=False)

order_placed_flag = False

class TrailingStopLoss:
    def __init__(self, initial_price, trailing_percentage):
        self.initial_price = initial_price
        self.trailing_percentage = trailing_percentage
        self.trailing_stop = initial_price * (1 - trailing_percentage / 100)
        self.highest_price = initial_price

    def update_price(self, current_price):
        # Update the highest price if the current price is higher
        if current_price > self.highest_price:
            self.highest_price = current_price
            self.trailing_stop = self.highest_price * (1 - self.trailing_percentage / 100)
        return self.trailing_stop

    def should_sell(self, current_price):
        # Check if the current price has hit the trailing stop
        return current_price <= self.trailing_stop

def place_orders(option):
        global order_placed_flag
        if not order_placed_flag:
            # Place Order
            res = breeze.place_order(stock_code=option["stock_code"],
                                    exchange_code="NFO",
                                    product="options",
                                    action="buy",
                                    order_type="market",
                                    stoploss="",
                                    quantity="25",  
                                    price="",
                                    validity="day",
                                    validity_date="2024-07-03T06:00:00.000Z",
                                    disclosed_quantity="0",
                                    expiry_date=option["expiry_date"],
                                    right=option["right"],
                                    strike_price=option["strike_price"])

            print(f"res:{res}")
            print("Call Buy Order Placed")
            order_id = res["Success"]["order_id"]
            print(f"order_id:{order_id}")
            order_placed_flag = True
            for _ in range(10):
                order_detail = breeze.get_order_detail(exchange_code="NFO", order_id=order_id)
                status = order_detail["Success"][0]["status"]
                if status == "Executed":
                    return order_detail
                time.sleep(1)
            
        return None


def calculate_pnl(initial_price, current_price):
    pnl = (current_price - initial_price) * quantity
    return pnl

def monitor_strategy():
    time.sleep(1)
    global running
    initial_price = None
    cumulative_pnl = 0
    trailing_stop_loss = None

    option = options_basket[0]
    
    while running:
        try:
            current_time = datetime.now().time()
            if current_time >= end_time:
                logger.info(f"End time reached")
                break

            with last_price_tick_lock:
                if last_price_tick is None:
                    continue
                current_price = last_price_tick

            if initial_price is None:
                order_detail = place_orders(option)
                if order_detail:
                    status = order_detail["Success"][0]["status"]
                    logger.info(f"status:{status}")
                    if status == "Executed":
                        initial_price = float(order_detail["Success"][0]["average_price"])
                        logger.info(f"Initial Price:{initial_price}")
                        trailing_stop_loss = TrailingStopLoss(initial_price, trailing_percentage)
                        logger.info(f"Trailing Stoploss:{trailing_stop_loss}")

            if trailing_stop_loss:
                
                trailing_stop = trailing_stop_loss.update_price(current_price)
                cumulative_pnl = calculate_pnl(initial_price, current_price)
                
                logger.info(f"Current Price: {current_price}, Trailing Stop: {trailing_stop}, PnL: {cumulative_pnl}")

                if trailing_stop_loss.should_sell(current_price):
                    logger.info(f"Trailing stop hit, selling at price: {current_price}")
                    # Execute sell logic here
                    # breeze.place_order(stock_code=option["stock_code"],
                    #                 exchange_code="NFO",
                    #                 product="options",
                    #                 action="sell",
                    #                 order_type="market",
                    #                 stoploss="",
                    #                 quantity="25",  
                    #                 price="",
                    #                 validity="day",
                    #                 validity_date="2024-07-03T06:00:00.000Z",
                    #                 disclosed_quantity="0",
                    #                 expiry_date=option["expiry_date"],
                    #                 right=option["right"],
                    #                 strike_price=option["strike_price"])
                    break

                if cumulative_pnl <= -max_loss:
                    logger.info(f"Max loss reached, exiting all positions at price: {current_price}")
                    # Execute exit logic here
                    # breeze.place_order(stock_code=option["stock_code"],
                    #                 exchange_code="NFO",
                    #                 product="options",
                    #                 action="sell",
                    #                 order_type="market",
                    #                 stoploss="",
                    #                 quantity="25",  
                    #                 price="",
                    #                 validity="day",
                    #                 validity_date="2024-07-03T06:00:00.000Z",
                    #                 disclosed_quantity="0",
                    #                 expiry_date=option["expiry_date"],
                    #                 right=option["right"],
                    #                 strike_price=option["strike_price"])
                    break

                if cumulative_pnl >= max_profit:
                    logger.info(f"Max profit reached, exiting all positions at price: {current_price}")
                    # Execute exit logic here
                    # breeze.place_order(stock_code=option["stock_code"],
                    #                 exchange_code="NFO",
                    #                 product="options",
                    #                 action="sell",
                    #                 order_type="market",
                    #                 stoploss="",
                    #                 quantity="25",  
                    #                 price="",
                    #                 validity="day",
                    #                 validity_date="2024-07-03T06:00:00.000Z",
                    #                 disclosed_quantity="0",
                    #                 expiry_date=option["expiry_date"],
                    #                 right=option["right"],
                    #                 strike_price=option["strike_price"])
                    break

        except KeyboardInterrupt:
            print("Exiting")
            running = False
        except Exception as ex:
            print(str(ex))
            running = False


# Start monitoring strategy
monitor_strategy()