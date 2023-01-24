#import required libraries
import base64 
import socketio

#Get User ID and Session Token
session_key = "SESSION_TOKEN_FROM_CUSTOMER_DETAILS_API"
#e.g session_key = "QUYyOTUzMTM6NjY5ODc5NzY="

user_id, session_token = base64.b64decode(session_key.encode('ascii')).decode('ascii').split(":")
#e.g Decoded value - AF296713:66987976, after split user_id = AF295313, session_token = 6698797

# Python Socket IO Client
sio = socketio.Client()
auth = {"user": user_id, "token": session_token}
sio.connect("https://livefeeds.icicidirect.com", headers={"User-Agent":"python-socketio[client]/socket"}, 
                auth=auth, transports="websocket", wait_timeout=3)

# Script Code of Stock or Instrument  e.g 4.1!1594, 1.1!500209 , 13.1!5023, 6.1!247457. 
script_code = ["one_click_fno"] #Subscribe more than one stock at a time

channel_name = 'stock'

#parsing logic 
def parse_data(data):

    if data and type(data) == list and len(data) > 0 and type(data[0]) == str and "!" not in data[0] and len(data) == 28:
        strategy_dict = dict()
        strategy_dict['strategy_date'] = data[0]
        strategy_dict['modification_date'] = data[1]
        strategy_dict['portfolio_id'] = data[2]
        strategy_dict['call_action'] = data[3]
        strategy_dict['portfolio_name'] = data[4]
        strategy_dict['exchange_code'] = data[5]
        strategy_dict['product_type'] = data[6]
        #strategy_dict['INDEX/STOCK'] = data[7]
        strategy_dict['underlying'] = data[8]
        strategy_dict['expiry_date'] = data[9]
        #strategy_dict['OCR_EXER_TYP'] = data[10]
        strategy_dict['option_type'] = data[11]
        strategy_dict['strike_price'] = data[12]
        strategy_dict['action'] = data[13]
        strategy_dict['recommended_price_from'] = data[14]
        strategy_dict['recommended_price_to'] = data[15]
        strategy_dict['minimum_lot_quantity'] = data[16]
        strategy_dict['last_traded_price'] = data[17]
        strategy_dict['best_bid_price'] = data[18]
        strategy_dict['best_offer_price'] = data[19]
        strategy_dict['last_traded_quantity'] = data[20]
        strategy_dict['target_price'] = data[21]           
        strategy_dict['expected_profit_per_lot'] = data[22]
        strategy_dict['stop_loss_price'] = data[23]
        strategy_dict['expected_loss_per_lot'] = data[24]
        strategy_dict['total_margin'] = data[25]
        strategy_dict['leg_no'] = data[26]
        strategy_dict['status'] = data[27]
        return(strategy_dict)

#CallBack functions to receive feeds
def on_ticks(ticks):
    ticks = parse_data(ticks)
    print(ticks)

#Connect to receive feeds
sio.emit('join', script_code)
sio.on(channel_name, on_ticks)

#Unwatch from the stock
sio.emit("leave", script_code)

#Disconnect from the server
sio.emit("disconnect", "transport close")
