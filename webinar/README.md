These are code files that we used in our webinars.

* breeze_webinar_20230215.py
  * get_names() example
  * place get_historical_data_v2() call and take data into a dataframe
  * preview_order() example

* breeze_webinar_auto_strike_selection_20230407.py
  * get_option_chain_quotes() used to download active option chain
  * weeding out illiquid strikes/contracts
  * strike/contract selection based on absolute number of strikes away
  * strike/contract selection based on greeks, with the example of Delta-based selection
  * [TBD] strike/contract selection based on premium we want to pay
 
* chatGPT.py
  * code generated by ChatGPT is operationalized by Breeze APIs to trade an intra-day short-straddle selling strategy
 
* data.py
  * simple sample code to place a single call to get_historical_data_v2() to get equity data and take into a Pandas dataframe
 
* how_to_calculate_sma.py
  * simple sample code to download stock data and apply a Simple Moving Average indicator to the data
 
* how_to_place_option_order.py
  * simple sample code to place a market order in a given options contract
 
* how_to_use_websockets.py
  * simple sample code to subscribe to live market feed for an options contract
 
* sdk_straddle.py
  * executing a stoploss-teke profit inclusive short straddle in JUST 14 lines of code, by using the breeze_strategies helper module

* trailing_stoploss.py
  * how to implement a trailing stoploss in a while loop
 
* Option_Plus.py
  * how to place and modify an OptionPlus order
 
* get_started.py
  * how to connect to Breeze API and place a simple stock buy market order