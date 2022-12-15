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
STOCK = "SUZENE"
TIME_GAP_IN_SECONDS = float(2)
QTY = 14
SLICE = float(3)
today = datetime.now()

START_TIME = today.replace(hour=17,
                           minute=42,
                           second=0, 
                           microsecond=0)

END_TIME = today.replace(hour=17,
                         minute=43,
                         second=0, 
                         microsecond=0)

ORDERBOOK=[]

def if_market_open():
    current_time = datetime.now()
    MARKET_OPEN = current_time.replace(hour=9,minute=15,second=0, microsecond=0)
    MARKET_CLOSE = current_time.replace(hour=15,minute=30,second=0, microsecond=0)

    try:
        assert (current_time > MARKET_OPEN) and (current_time < MARKET_CLOSE)
        print("Market is Open right now !!")    
        return True

    except Exception as e:
        print("Market is Closed right now !!")    
        return False
        
def get_current_price():
    #This function fetches the last traded price (LTP) of stock
    global STOCK
    try:
        price = breeze.get_quotes(stock_code=STOCK,exchange_code="NSE",product_type="cash")
        ltp = price['Success'][0]['ltp']
        return round(ltp*0.97,1)

    except Exception as error:
        print('Failed Quotes API request', error)
        
def place_buy_order(limit_price):
    global QTY,SLICE, STOCK
    

    if (QTY > 0 and QTY < SLICE): 
        SLICE = QTY%SLICE
        QTY=0

    current_time = datetime.now()
    print(f"Buying {SLICE} shares of {STOCK} at time {current_time.strftime('%H:%M:%S')}")

    try:
        buy_order = breeze.place_order(stock_code=STOCK,
                    exchange_code="NSE",
                    product="cash",
                    action="buy",
                    order_type="limit",
                    stoploss="",
                    quantity=SLICE,
                    price=limit_price,
                    validity="day")

        if(buy_order['Status']==200) :
            QTY -= SLICE
            order_id = buy_order['Success']['order_id']
            print(f'Successfully placed limit order at {limit_price} \nOrder ID is {order_id}\n')
            orderbook.append(order_id)

        else : 
            print('Failed to place order', buy_order)

    except Exception as error:
        print('Failed Place Order API Request', error)

def start_strategy(duration):
    # This function starts strategy for 'duration' seconds provided by user
        
    global ORDERBOOK, START_TIME, END_TIME, STOCK, QTY, SLICE
    ORDERBOOK = []
    
    # Set current_time
    current_time = datetime.now()
        
    #check if current time is not more than end time otherwise exit alog
    while(current_time > END_TIME):
        print('Current Time is more than End Time\nExiting Algo !!')
        return

    #check if current time is not less than start time otherwise wait
    while(current_time < START_TIME):
        wait_time = (START_TIME - datetime.now()).seconds
        print(f"Start Time : {START_TIME.strftime('%H:%M:%S')}\nCurrent_time :{current_time.strftime('%H:%M:%S')}\nWaiting Time : {wait_time} seconds")
        time.sleep(wait_time+1)
        current_time = datetime.now()
            
    current_time = datetime.now()
              
    print(f"\nTWAP started at {current_time.strftime('%H:%M:%S')}\n")              

    # if current time is correct : Start the loop
    while (current_time > START_TIME and current_time < END_TIME and QTY > 0):
        limit_price = get_current_price()
        place_buy_order(limit_price)
        
        # Pause for TIME_GAP_IN_SECONDS and then reset the current time for next iteration
        time.sleep(TIME_GAP_IN_SECONDS)
        
        #reset current time
        current_time = datetime.now()
        
    current_time = datetime.now()
    print(f"/nTWAP is complete.\nPending Orders are : {QTY}\nCurrent Time is : {current_time.strftime('%H:%M:%S')}")
    exit()

if __name__ == "__main__":
    while(if_market_open()):
        start_strategy(20)
        break
        
