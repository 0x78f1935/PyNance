class Orders(object):
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    def open_orders(self, **params):
        """[summary]

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        Returns:
            [list]: 
        """
        data = self.client.get(f'{self.client.endpoint}/api/v3/openOrders', signed=True, data=params)
        if data.isSucces: return data.json
        return []
