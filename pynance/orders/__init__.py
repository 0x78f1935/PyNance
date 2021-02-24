from pynance.core.exceptions import BinanceException

class Orders(object):
    def __init__(self, client):
        self.client = client
    
    def open(self, asset=None):
        """Retrieves a collection of all open orders

        Example
            client.orders.open() # or
            client.orders.open('LTCBTC')
        """
        if asset is None: _filter = {}
        else: _filter = {'symbol': asset}
        return self.client.get(f'{self.client.endpoint}/api/v3/openOrders', signed=True, data=_filter)

    def create(self, asset=None, quantity=None, buy=True, stop_price=None, test=False):
        """This method is able to create different kind of buy/sell order on market value.
        Stop limit / take profit is supported if the stop_price is provided.
        Based on the buy boolean the stop_price will be set accordingly.
        
        Args:
            asset (string): The coin which we are currently trading
            quantity (float): The total amount you would like to trade.
            buy (bool, optional): When False the order will be a sell order. Defaults to True.
            stop_price (float, optional): When provided a stop/take profit will be set.
                                          When buy is True take profit will be set
                                          when buy is False stop loss will be set
                                          Defaults to None.
            test (bool, optional): When True the order will be created in the test environment. 
                                   Defaults to False.

        Raises:
            BinanceException: Happens when asset or quantity is not provided
        """
        if asset is None or quantity is None: raise BinanceException("Asset and quantity are required")
        _filter = {"symbol":asset, "quantity": quantity}
        if buy: side = "BUY"
        else: side = "SELL"
        _filter['side'] = side
        if stop_price is None: _filter['type'] = "MARKET"
        else:
           if buy: buy_type = "TAKE_PROFIT" 
           else: buy_type = "STOP_LOSS"
           _filter['type'] = buy_type
           _filter['stopPrice'] = stop_price
        
        if test: endpoint = f'{self.client.endpoint}/api/v3/order/test'
        else: endpoint = f'{self.client.endpoint}/api/v3/order'
        return self.client.post(endpoint, signed=True, data=_filter)
