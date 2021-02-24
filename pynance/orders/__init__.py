class Orders(object):
    def __init__(self, client):
        self.client = client
    
    def open_orders(self, asset=None):
        """Retrieves a collection of all open orders

        Example
            client.orders.open_orders() # or
            client.orders.open_orders('LTCBTC')
        """
        if asset is None: _filter = {}
        else: _filter = {'symbol': asset}
        return self.client.get(f'{self.client.endpoint}/api/v3/openOrders', signed=True, data=_filter)
