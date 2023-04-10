The idea is to receive json structures that are basically breeze.place_order() calls + a secret. If the secret matches, then the server sends a place order call over breeze. JSON can be created referring to [PyPi's place_order() documentation](https://pypi.org/project/breeze-connect/#place_order). Some examples are:

    breeze.place_order(stock_code="ICIBAN",
                    exchange_code="NFO",
                    product="futures",
                    action="buy",
                    order_type="limit",
                    stoploss="0",
                    quantity="3200",
                    price="200",
                    validity="day",
                    validity_date="2022-08-22T06:00:00.000Z",
                    disclosed_quantity="0",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    right="others",
                    strike_price="0",
                    user_remark="Test")
                    
will translate to the following JSON:
      '{"stock_code":"ICIBAN","exchange_code":"NFO","product":"futures","action":"buy","order_type":"limit","stoploss":"0","quantity":"3200","price":"200","validity":"day","validity_date":"2022-08-22T06:00:00.000Z","disclosed_quantity":"0","expiry_date":"2022-08-25T06:00:00.000Z","right":"others","strike_price":"0","user_remark":"Test","secret":"whatever_i_want"}'
      
where the `'secret'` is defined by you in your code.
