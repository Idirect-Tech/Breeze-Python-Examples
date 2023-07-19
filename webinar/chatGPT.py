#Configure the strategy using API Keys and set stoploss/takeprofit level.
api_key = "YOUR_APP_KEY"
api_secret = "YOUR_SECRET_KEY"
api_session = 'YOUR_SESSION_KEY'

#Import the library
from breeze_connect import BreezeConnect

#Create API library object
api = BreezeConnect(api_key=api_key)
api.generate_session(api_secret=api_secret,session_token=api_session)

# Function to place a straddle. Make sure to change the contract details i.e. expiry_date, vailidity_date, strike_price, quantity etc.
def place():
    
    for option_type in ['call','put']:
        response = api.place_order(stock_code="NIFTY",
                        exchange_code="NFO",
                        product="options",
                        action="buy",
                        order_type="market",
                        stoploss="",
                        quantity="50",
                        price="",
                        validity="day",
                        validity_date="2023-07-19T06:00:00.000Z",
                        disclosed_quantity="0",
                        expiry_date="2023-07-20T06:00:00.000Z",
                        right= option_type,
                        strike_price="19800")
        print(response)


# Function to square off a straddle. Make sure to change the action to 'buy' or 'sell' depending upon open position. 
def squareoff():
    
    for option_type in ['call','put']:
        response = api.square_off(exchange_code="NFO",
                            product="options",
                            stock_code="NIFTY",
                            expiry_date="2023-07-20T06:00:00.000Z",
                            right=option_type,
                            strike_price="19800",
                            action="sell",
                            order_type="market",
                            validity="day",
                            stoploss="0",
                            quantity="50",
                            price="0",
                            validity_date="2023-07-19T06:00:00.000Z",
                            trade_password="",
                            disclosed_quantity="0")        
        
        print(response)   

# Function to calculate P&L
def calculate_pnl():
    
    pnl = 0
    response = api.get_portfolio_positions()

    if response['Status'] == 200:
        response = response['Success']

        for item in response:
            ltp = float(item['ltp'])
            cost = float(item['average_price'])
            qty = int(item['quantity'])
            # print((item['ltp'],item['average_price']))
            pnl += round((ltp - cost)*qty, 2)     

    print(f"P&L : {pnl}")
    return pnl


# Function to check if market is open
def is_market_open():
    current_time = datetime.datetime.now().time()
    market_open_time = datetime.time(9, 15)  # Assuming market opens at 9:15 AM
    market_close_time = datetime.time(15, 30)  # Assuming market closes at 3:30 PM
    return market_open_time <= current_time <= market_close_time

# Function to place a short straddle
def place_straddle():
    # Code to place the straddle order goes here
    place()
    print("Long straddle order placed.")

# Function to square off the position
def square_off_position():
    # Code to square off the position goes here
    squareoff()
    print("Position squared off.")

# Function to square off the position
def profit_or_loss_threshold_reached():
    # Code to calculate PnL
    print("\nCHECKING P&L...")
    pnl = calculate_pnl()
    if pnl < -100:
        return True
    else:
        return False
    
    
# Main function
def main():
    
    # Place the straddle
    place_straddle()

    print("Waiting for 3 seconds for order execution")
    time.sleep(3)
    
    while is_market_open():
        # Check if profit or loss threshold is reached
        # Replace the condition below with your own logic
        if profit_or_loss_threshold_reached():
            square_off_position()
            break

        print("Waiting for 20 seconds for P&L check")
        time.sleep(60)  # Sleep for 60 seconds before checking again

if __name__ == "__main__":
    main()
