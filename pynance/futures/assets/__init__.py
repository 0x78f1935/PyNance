class Assets(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#general-info

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client

    def symbols(self, symbol=None):
        """Latest price for a symbol or symbols.

        Args:
            symbol (string, optional): [When provided returns information about that symbol]. Defaults to None.
        """
        endpoint = "https://fapi.binance.com/fapi/v1/ticker/price"
        if symbol is None: data = self.client._get(endpoint, False)
        else: data = self.client._get(endpoint, False, data={'symbol': symbol})
        self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
        return data
    
    def exchange_info(self, symbols:list=[]):
        """Get information about the exchange or about a certian asset
        Args:
            symbol (string, optional): A trade currency. Defaults to None.
                                        If None returns info about the exchange and all the coins
                                        If provided it will return only info about the coin.
        """
        endpoint = "https://fapi.binance.com/fapi/v1/exchangeInfo"
        if not symbols: 
            data = self.client._get(endpoint, signed=False)
        else:
            data = self.client._get(endpoint, signed=False)
            data.json['symbols'] = [i for i in data.json['symbols'] if i['symbol'] in symbols]
        self.client.logger.info(f'Weight: {data.info["weight"]} / 1200')
        return data

