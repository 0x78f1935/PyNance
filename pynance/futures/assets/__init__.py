class Assets(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#general-info

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client

    def symbols(self, symbol:str=None):
        """Latest price for a symbol or symbols.

        Args:
            symbol (string, optional): [When provided returns information about that symbol]. Defaults to None.
        """
        endpoint = "https://fapi.binance.com/fapi/v1/ticker/price"
        if symbol is None: data = self.client._get(endpoint, False)
        else: data = self.client._get(endpoint, False, data={'symbol': symbol})
        self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
        return data

    def best_price_qty(self, symbol:str=None):
        """Best price/qty on the order book for a symbol or symbols.

        Args:
            symbol (string, optional): [target symbol]. Defaults to None.

        Returns:
            [Response Object]: [PyNance response object]
        """
        endpoint = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
        data = self.client._get(endpoint, False)
        if symbol is not None: 
            raw = [i for i in data.json if i['symbol'] == symbol]
            if raw: data = data._update_data({'_data': raw})
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

    def klines(self, symbol="BTCUSDT", timeframe="1h", total_candles=500):
        """Returns information based on the provided symbol
        
        Args:
            symbol (str, optional): [Symbol]. Defaults to "BTCUSDT".
            timeframe (str, optional): [timeframe which is also available in binance graphs]. Defaults to "1h".
            total_candles (int, optional): [total amount of candles to return]. Defaults to 500.

        Returns:
            [list]: [The list can be used in candle charts for example]

            [
                [
                    1598371200000,      // Open time
                    "5.88275270",       // Open NAV price
                    "6.03142087",       // Highest NAV price
                    "5.85749741",       // Lowest NAV price
                    "5.99403551",       // Close (or the latest) NAV price
                    "2.28602984",       // Real leverage
                    1598374799999,      // Close time
                    "0",                // Ignore
                    6209,               // Number of NAV update
                    "14517.64507907",   // Ignore
                    "0",                // Ignore
                    "0"                 // Ignore
                ]
            ]
        """
        endpoint = "https://fapi.binance.com/fapi/v1/lvtKlines"
        data = self.client._get(
            endpoint,
            False, 
            data={
                "symbol": symbol,
                "interval": timeframe,
                "limit": total_candles,
            }
        )
        self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
        klines = data.json
        if len(klines) >= 1: klines = [[float(o) for o in i] for i in klines]
        return klines
