#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

#make sure to install latest library of Breeze using --> pip install --upgrade breeze-connect 
from breeze_connect import BreezeConnect 
import json
import http.client
import base64 
import hashlib
import datetime

# Create session object
breeze = BreezeConnect(api_key=api_key)
breeze.generate_session(api_secret=api_secret,session_token=api_session)

#base URL
conn = http.client.HTTPSConnection("api.icicidirect.com")

# Customer Details API
payload = {
    'SessionToken': api_session,
    'AppKey': api_key
}

headers = {"Content-Type": "application/json"}

conn.request("GET", "/breezeapi/api/v1/customerdetails", str(payload), headers)
res = conn.getresponse()
data = res.read()
print('\nCustomer Details API Response:\n')
print(data.decode("utf-8"))

# Store Session_Token
session_token = json.loads(data.decode("utf-8"))
session_token = session_token['Success']['session_token']

# Option Chain API

# 'body' is the request-body of your current request
body = {"stock_code": "NIFTY",
        "exchange_code": "NFO",
        "expiry_date": "2023-03-02T06:00:00.000Z",
        "product_type": "options",
        "right": "call",
        "strike_price": "19000"
}

payload = json.dumps(body, separators=(',', ':'))

#time_stamp & checksum generation for request-headers
time_stamp = datetime.datetime.utcnow().isoformat()[:19] + '.000Z'
checksum = hashlib.sha256((time_stamp+payload+api_secret).encode("utf-8")).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-Checksum': 'token '+checksum,
    'X-Timestamp': time_stamp,
    'X-AppKey': api_key,
    'X-SessionToken': session_token
}

conn.request("GET", "/breezeapi/api/v1/optionchain", payload, headers)
res = conn.getresponse()
data = res.read()
print('\nOption Chain API Response:\n')
print(data.decode("utf-8"))



