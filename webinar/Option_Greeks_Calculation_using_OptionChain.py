from breeze_connect import BreezeConnect
import urllib
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.numerical import delta, gamma, theta, vega, rho
from scipy.optimize import brentq
import numpy as np
from datetime import datetime

#Connecting to Breeze 
breeze = BreezeConnect(api_key=str(app_key))

print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(str(app_key)))

breeze.generate_session(api_secret=str(secret_key),session_token=str(session_key))

#Finding price of an option

#call

S = 24117  # Underlying asset price
K_call = 24150  # Option strike price
t = 7/365  # Time to expiration in years
r = 0.10  # Risk-free interest rate
sigma_call = 0.13  # Volatility
flag_call = 'c'  # 'c' for Call, 'p' for Put

# Option price
option_price_call = black_scholes(flag_call, S, K_call, t, r, sigma_call)
print("Option Price_Call:", option_price_call)

#Put

S = 24117  # Underlying asset price
K_put = 24150  # Option strike price
t = 7/365  # Time to expiration in years
r = 0.10  # Risk-free interest rate
sigma_put = 0.17  # Volatility
flag_put = 'p'  # 'c' for Call, 'p' for Put

# Option price
option_price_put = black_scholes(flag_put, S, K_put, t, r, sigma_put)
print("Option Price_Put:", option_price_put)

#Finding Greeks of an option

#Put

# Delta
delta_value_put = delta(flag_put, S, K_put, t, r, sigma_put)
print("Delta_put:", delta_value_put)

# Gamma
gamma_value_put = gamma(flag_put, S, K_put, t, r, sigma_put)
print("Gamma_put:", gamma_value_put)

# Theta
theta_value_put = theta(flag_put, S, K_put, t, r, sigma_put)
print("Theta_put:", theta_value_put)

# Vega
vega_value_put = vega(flag_put, S, K_put, t, r, sigma_put)
print("Vega_put:", vega_value_put)

# Rho
rho_value_put = rho(flag_put, S, K_put, t, r, sigma_put)
print("Rho_put:", rho_value_put)

#call

# Delta
delta_value_call = delta(flag_call, S, K_call, t, r, sigma_call)
print("Delta_call:", delta_value_call)

# Gamma
gamma_value_call =gamma(flag_call, S, K_call, t, r, sigma_call)
print("Gamma_call:", gamma_value_call)

# Theta
theta_value_call = theta(flag_call, S, K_call, t, r, sigma_call)
print("Theta_call:", theta_value_call)

# Vega
vega_value_call = vega(flag_call, S, K_call, t, r, sigma_call)
print("Vega_call:", vega_value_call)

# Rho
rho_value_call = rho(flag_call, S, K_call, t, r, sigma_call)
print("Rho_call:", rho_value_call)

# Calculating Option Greeks in Option Chain


#find ATM strike Price
Quotes = breeze.get_quotes(stock_code="NIFTY",
                    exchange_code="NSE",
                    expiry_date="",
                    product_type="cash",
                    right="",
                    strike_price="")

Spot = Quotes["Success"][0]["ltp"]
ATM = round((Quotes["Success"][0]["ltp"])/50)*50
print(ATM)


# Simulate the data retrieval from breeze for Call
df = breeze.get_option_chain_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date="2024-08-14T06:00:00.000Z",
                    right="call")["Success"]

# Convert to DataFrame
df = pd.DataFrame(df)

# Convert strike_price to float
df['strike_price'] = df['strike_price'].astype(float)

# Define target strike and range parameters
target_strike = ATM
strike_increment = 50
range_size = 5

# Define the range for strike prices
lower_bound = target_strike - range_size * strike_increment
upper_bound = target_strike + range_size * strike_increment

# Filter the rows where the strike price is within the range and in increments of 50
filtered_df = df[(df['strike_price'] >= lower_bound) & 
                 (df['strike_price'] <= upper_bound) & 
                 (df['strike_price'] % strike_increment == 0)]

# Print the filtered DataFrame to debug
#print("Filtered DataFrame:", filtered_df[['strike_price']])

# Check if any rows match the criteria
if filtered_df.empty:
    print("No strike prices found within the specified range.")
else:
    # Sort by strike price
    sorted_df = filtered_df.sort_values('strike_price').reset_index(drop=True)

    # Check if the target_strike exists
    if target_strike in sorted_df['strike_price'].values:
        target_index = sorted_df[sorted_df['strike_price'] == target_strike].index[0]

        # Slice the DataFrame to get 5 rows above and 5 rows below the target
        start_index = max(0, target_index - 5)
        end_index = min(len(sorted_df), target_index + 6)
        final_df = sorted_df.iloc[start_index:end_index]

        # Select only the required columns
        final_df = final_df[['stock_code', 'expiry_date', 'right', 'strike_price', 'ltp']]
  
        # Define constants for Greeks calculation
        risk_free_rate = 0.05  # Example risk-free rate (5%)

        # Add spot price column for the calculation
        final_df['spot_price'] = Spot  # Example spot price

        # Function to calculate implied volatility using LTP
        def calculate_implied_volatility(row):
            S = row['spot_price']  # Spot price
            K = row['strike_price']  # Strike price
            T = (pd.to_datetime(row['expiry_date']) - pd.Timestamp.now()).days / 365  # Time to expiration in years
            r = risk_free_rate  # Risk-free rate
            option_price = row['ltp']  # Last traded price
            right = row['right'].lower()  # 'call' or 'put'

            # Define the function to calculate implied volatility
            def objective_function(sigma):
                if right == 'call':
                    option_type = 'c'
                elif right == 'put':
                    option_type = 'p'
                else:
                    raise ValueError("Invalid option type")

                return black_scholes(option_type, S, K, T, r, sigma) - option_price
            
            # Solve for implied volatility
            try:
                implied_vol = brentq(objective_function, 0.01, 5.0)
            except ValueError:
                implied_vol = np.nan
            return implied_vol

        # Calculate implied volatility and add to DataFrame
        final_df['implied_volatility'] = final_df.apply(calculate_implied_volatility, axis=1)

        # Function to calculate Greeks
        def calculate_greeks(row):
            S = row['spot_price']  # Spot price
            K = row['strike_price']  # Strike price
            T = (pd.to_datetime(row['expiry_date']) - pd.Timestamp.now()).days / 365  # Time to expiration in years
            r = risk_free_rate  # Risk-free rate
            sigma = row['implied_volatility']  # Implied volatility
            right = row['right'].lower()  # 'call' or 'put'

            if right == 'call':
                option_type = 'c'
            elif right == 'put':
                option_type = 'p'
            else:
                raise ValueError("Invalid option type")

            # Calculate Greeks using py_vollib
            delta_value = delta(option_type, S, K, T, r, sigma)
            gamma_value = gamma(option_type, S, K, T, r, sigma)
            theta_value = theta(option_type, S, K, T, r, sigma)
            vega_value = vega(option_type, S, K, T, r, sigma)
            rho_value = rho(option_type, S, K, T, r, sigma)
            
            return pd.Series([delta_value, gamma_value, theta_value, vega_value, rho_value], 
                             index=['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'])

        # Calculate Greeks and add to DataFrame
        greeks_df = final_df.apply(calculate_greeks, axis=1)
        result_df = pd.concat([final_df, greeks_df], axis=1)

        # Round the values
        result_df['implied_volatility'] = result_df['implied_volatility'].round(2)
        result_df['Delta'] = result_df['Delta'].round(2)
        result_df['Theta'] = result_df['Theta'].round(2)
        result_df['Vega'] = result_df['Vega'].round(2)
        result_df['Rho'] = result_df['Rho'].round(2)

        # Print the resulting DataFrame with Greeks
        print("Final DataFrame with Greeks for Call:")
        print(result_df)
    else:
        print(f"Strike price {target_strike} not found in the filtered data.")

# Option greeks for Put

df = breeze.get_option_chain_quotes(stock_code="NIFTY",
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date="2024-08-14T06:00:00.000Z",
                    right="put")["Success"]

# Convert to DataFrame
df = pd.DataFrame(df)

# Convert strike_price to float
df['strike_price'] = df['strike_price'].astype(float)

# Define target strike and range parameters
target_strike = ATM
strike_increment = 50
range_size = 5

# Define the range for strike prices
lower_bound = target_strike - range_size * strike_increment
upper_bound = target_strike + range_size * strike_increment

# Filter the rows where the strike price is within the range and in increments of 50
filtered_df = df[(df['strike_price'] >= lower_bound) & 
                 (df['strike_price'] <= upper_bound) & 
                 (df['strike_price'] % strike_increment == 0)]

# Print the filtered DataFrame to debug
#print("Filtered DataFrame:", filtered_df[['strike_price']])

# Check if any rows match the criteria
if filtered_df.empty:
    print("No strike prices found within the specified range.")
else:
    # Sort by strike price
    sorted_df = filtered_df.sort_values('strike_price').reset_index(drop=True)

    # Check if the target_strike exists
    if target_strike in sorted_df['strike_price'].values:
        target_index = sorted_df[sorted_df['strike_price'] == target_strike].index[0]

        # Slice the DataFrame to get 5 rows above and 5 rows below the target
        start_index = max(0, target_index - 5)
        end_index = min(len(sorted_df), target_index + 6)
        final_df = sorted_df.iloc[start_index:end_index]

        # Select only the required columns
        final_df = final_df[['stock_code', 'expiry_date', 'right', 'strike_price', 'ltp']]

        # Define constants for Greeks calculation
        risk_free_rate = 0.05  # Example risk-free rate (5%)

        # Add spot price column for the calculation
        final_df['spot_price'] = Spot  # Example spot price

        # Function to calculate implied volatility using LTP
        def calculate_implied_volatility(row):
            S = row['spot_price']  # Spot price
            K = row['strike_price']  # Strike price
            T = (pd.to_datetime(row['expiry_date']) - pd.Timestamp.now()).days / 365  # Time to expiration in years
            r = risk_free_rate  # Risk-free rate
            option_price = row['ltp']  # Last traded price
            right = row['right'].lower()  # 'call' or 'put'

            # Define the function to calculate implied volatility
            def objective_function(sigma):
                if right == 'call':
                    option_type = 'c'
                elif right == 'put':
                    option_type = 'p'
                else:
                    raise ValueError("Invalid option type")

                return black_scholes(option_type, S, K, T, r, sigma) - option_price
            
            # Solve for implied volatility
            try:
                implied_vol = brentq(objective_function, 0.01, 5.0)
            except ValueError:
                implied_vol = np.nan
            return implied_vol

        # Calculate implied volatility and add to DataFrame
        final_df['implied_volatility'] = final_df.apply(calculate_implied_volatility, axis=1)

        # Function to calculate Greeks
        def calculate_greeks(row):
            S = row['spot_price']  # Spot price
            K = row['strike_price']  # Strike price
            T = (pd.to_datetime(row['expiry_date']) - pd.Timestamp.now()).days / 365  # Time to expiration in years
            r = risk_free_rate  # Risk-free rate
            sigma = row['implied_volatility']  # Implied volatility
            right = row['right'].lower()  # 'call' or 'put'

            if right == 'call':
                option_type = 'c'
            elif right == 'put':
                option_type = 'p'
            else:
                raise ValueError("Invalid option type")

            # Calculate Greeks using py_vollib
            delta_value = delta(option_type, S, K, T, r, sigma)
            gamma_value = gamma(option_type, S, K, T, r, sigma)
            theta_value = theta(option_type, S, K, T, r, sigma)
            vega_value = vega(option_type, S, K, T, r, sigma)
            rho_value = rho(option_type, S, K, T, r, sigma)
            
            return pd.Series([delta_value, gamma_value, theta_value, vega_value, rho_value], 
                             index=['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'])

        # Calculate Greeks and add to DataFrame
        greeks_df = final_df.apply(calculate_greeks, axis=1)
        result_df = pd.concat([final_df, greeks_df], axis=1)

        # Round the values
        result_df['implied_volatility'] = result_df['implied_volatility'].round(2)
        result_df['Delta'] = result_df['Delta'].round(2)
        result_df['Theta'] = result_df['Theta'].round(2)
        result_df['Vega'] = result_df['Vega'].round(2)
        result_df['Rho'] = result_df['Rho'].round(2)

        # Print the resulting DataFrame with Greeks
        print("Final DataFrame with Greeks for Put:")
        print(result_df)
    else:
        print(f"Strike price {target_strike} not found in the filtered data.")
