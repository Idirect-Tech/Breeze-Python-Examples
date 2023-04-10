from breeze_connect import BreezeConnect
from flask import Flask, request
import sys      #to import configurations like keys

sys.path.append('/path/to/this/file/')

from breeze_configs import Breeze_Configs
configs = Breeze_Configs()

#set secret
webhook_secret='whatever_i_want'

try:
    breeze = BreezeConnect(api_key=configs.webhook_api_key)
    breeze.generate_session(api_secret=configs.webhook_api_secret, session_token=configs.webhook_session_token)
    breeze.ws_connect()
    breeze.subscribe_feeds(get_order_notification=True)
except Exception as e:
    print(e)

# create the Flask app
app = Flask(__name__)

@app.route('/place_order', methods=['POST'])
def json_example():
    request_data = request.get_json()
    if request_data:
        if request_data.pop('secret')==webhook_secret:
            try:
                dict_order_details = breeze.place_order(**request_data)
                print(dict_order_details)
                return dict_order_details
            except Exception as e:
                print(e)
                return e
        else:
            print("Authorization error: check credentials.")
            return "Authorization error: check credentials."
    else:
        return 'No data found.'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
