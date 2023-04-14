#intialize keys

api_key = "INSERT_YOUR_APP_KEY_HERE"
api_secret = "INSERT_YOUR_SECRET_KEY_HERE"
api_session = 'INSERT_YOUR_API_SESSION_HERE'

# This function installs Breeze library
def install():
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', 'breeze_connect'], stdout=subprocess.DEVNULL)
    print('Successfully installed Breeze !!')

# Import necessary libraries
import sys, subprocess, pkg_resources
module=True

while(module):
    try:
        from breeze_connect import BreezeConnect
        module=False
    except ModuleNotFoundError:
        print("module 'breeze_connect' is not installed. Installing it now...")    
        install()

try:
    # Connecting to demat account 
    api = BreezeConnect(api_key=api_key)
    api.generate_session(api_secret=api_secret,session_token=api_session)
    print("Successfully connected to demat account !!")    
    
except NameError:
    print("Connection to demat account failed !!")
    
try:
    
    funds = api.get_funds()
    
    if(funds['Status'] == 200):
      account = funds['Success']['bank_account']
      balance = funds['Success']['total_bank_balance']
      print(f"Account Number : {account},\nBank Balance: {balance}")
        
    else:
        print(funds['Error'])
            
except Exception as e:
    print("API request failed. Please try again !!/n", e)
