# The Idea

The idea is to receive JSON structures that are basically breeze.place_order() calls + a secret. If the secret matches, then the server sends a place order call over breeze. JSON can be created referring to [PyPi's place_order() documentation](https://pypi.org/project/breeze-connect/#place_order). 

# Examples

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
          `'{"stock_code":"ICIBAN","exchange_code":"NFO","product":"futures","action":"buy","order_type":"limit","stoploss":"0","quantity":"3200","price":"200","validity":"day","validity_date":"2022-08-22T06:00:00.000Z","disclosed_quantity":"0","expiry_date":"2022-08-25T06:00:00.000Z","right":"others","strike_price":"0","user_remark":"Test","secret":"whatever_i_want"}'`
      
where the `'secret'` is defined by you in your code, and is the only thing not used in the `place_order()` call. This is a **must** have because it's the only thing that prevents random people sending your server an instruction to place order.

# Notes

* Currently, this JSON needs to be sent to port 5000 of the web application's host. Once Gunicorn+nginx are added, we can then use port 80 and 443 like civilized human beings of culture. Don't try to force the app to serve on 80 (with `port=5000` changed to 80): best case scenario is that you will get an error, worst case is that you will negatively impact something already being served on port 80.
* Following best practices, we place credentials in a dedicated class in a separate file named `breeze_configs.py` in the same directory as the application code. We instantiate an object from that class, then use the init variables.
* Note the elegant use of *JSON -> dictionary -> kwargs*. This has been my biggest learning, and it came by a fluke: I just randomly thought that if \**kwargs can be used to denote an arbitrary dictionary of keyword arguments, it should apply in reverse as well. And it does! So first we transition from _JSON -> dictionary_ with `request.get_json()`, and then we transition from _dictionary -> kwargs_ with `place_order(**request_data)`. Smooth operator \*\*!


# TODOs
## Functionlity:
1. Front end to show events (maybe use [Flask Turbo](https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask) by none other than Miguel Grinberg)
2. Order updates refreshes on front end (i.e. pipe order update socket.io to front end above)
3. Connectivity monitoring

## Deployment:
1. Gunicorn
2. nginx
3. Docker
