from pynance.core.exceptions import PyNanceException
from statistics import mean


class Assets(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#change-log

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
        self.client.logger.info(f'Weight: {data.info["weight"]}')
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
            raw = [{
                'symbol': i['symbol'] if 'symbol' in i.keys() else None,
                'bidPrice': float(i['bidPrice']) if 'bidPrice' in i.keys() else 0,
                'bidQty': float(i['bidQty']) if 'bidQty' in i.keys() else 0,
                'askPrice': float(i['askPrice']) if 'askPrice' in i.keys() else 0,
                'askQty': float(i['askQty']) if 'askQty' in i.keys() else 0,
                'time': i['time'] if 'time' in i.keys() else 0,
            } for i in data.json if i['symbol'] == symbol]
            if raw: data = data._update_data({'_data': raw})
        self.client.logger.info(f'Weight: {data.info["weight"]}')
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

    def average(self, asset, timeframe=None, total_candles=60, low=True):
        """returns the price of any asset

        Parameters
            asset : str
                Represents the symbol
        
            timeframe : str
                Has to be one of the following: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
                Default: 1m

            total_candles: int
                The total amount of history candles to take in consideration. Max 1000
                default: 60
                When the total_candles is set to 60 and the timeframe is set to 1m you will get the average calculated
                over each minute in the last hour.
            
            low: bool
                The type of average we want to return. If low is True it takes the average of the lowest point of each candle.
                Otherwise the highest point of each candle will be used to calculate the average on
                default: True
                
        
        Example
            client.price.average('LTCBTC')
        """
        endpoint = "https://fapi.binance.com/fapi/v1/klines"
        if timeframe is None: timeframe = "1m"
        if timeframe not in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']: 
            raise PyNanceException("Timeframe is unknown, use one of the following timeframes: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']")

        data = self.client._get(
            endpoint,
            False, 
            data={
                "symbol": asset,
                "interval": timeframe,
                "limit": total_candles
            }
        )
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        expanded = [{
            "open time": i[0],
            "open": i[1],
            "high": i[2],
            "low": i[3],
            "close": i[4],
            "volume": i[5],
            "close time": i[6],
            "quote asset volume": i[7],
            "number of trades": i[8],
            "taker buy base asset volume": i[9],
            "taker buy quote asset volume": i[10],
            "ignore.": i[11]
        } for i in data.json]
        if low: return mean([float(i["low"]) for i in expanded])
        else: return mean([float(i["high"]) for i in expanded])

    def klines(self, symbol="BTCUSDT", timeframe="1h", total_candles=500):
        """Returns information based on the provided symbol
        
        Args:
            symbol (str, optional): [Symbol]. Defaults to "BTCUSDT".
            timeframe (str, optional): [timeframe which is also available in binance graphs]. Defaults to "1h".
            total_candles (int, optional): [total amount of candles to return]. Defaults to 500. Max 1000

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
        if timeframe not in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']: 
            raise PyNanceException("Timeframe is unknown, use one of the following timeframes: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']")
        if total_candles <= 0 or total_candles > 1000: raise PyNanceException("Total amount of candles needs to be between 1 and 1000")
        endpoint = "https://fapi.binance.com/fapi/v1/klines"
        data = self.client._get(
            endpoint,
            False, 
            data={
                "symbol": symbol,
                "interval": timeframe,
                "limit": total_candles,
            }
        )
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        klines = data.json
        if len(klines) >= 1: klines = [[float(o) for o in i if type(o) in [int, float]] for i in klines]
        return klines

    def volume(self, symbol:str="BTCUSDT", period:str="1h", limit:int=30):
        """Fetch Buy / Sell voume information

        Args:
            symbol (str, required): [Target symbol]. Defaults to "BTCUSDT".
            period (str, required): [Period]. Defaults to "1h". Available: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]

            limit (int, optional): [description]. Defaults to 30. Max 500

        Raises:
            PyNanceException: [description]
        """
        if symbol is None: raise PyNanceException('Provide a valid symbol')
        if period is None: raise PyNanceException('Provide a valid period: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]')
        if period not in ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]:
            raise PyNanceException('Period is unknown, use one of the following periods: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"]')
        if limit <= 0 or limit > 500: raise PyNanceException('Volume limit has to be between 1 and 500')
        endpoint = "https://fapi.binance.com/futures/data/takerlongshortRatio"
        data = self.client._get(
            endpoint,
            False, 
            data={
                "symbol": symbol,
                "period": period,
                "limit": limit,
            }
        )
        raw = [{
            'buySellRatio': float(i['buySellRatio']) if 'buySellRatio' in i.keys() else 0,
            'sellVol': float(i['sellVol']) if 'sellVol' in i.keys() else 0,
            'buyVol': float(i['buyVol']) if 'buyVol' in i.keys() else 0,
            'timestamp': i['timestamp'] if 'timestamp' in i.keys() else 0,
        } for i in data.json]
        if raw: data = data._update_data({'_data': raw})
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data

    def mark_price(self, symbol:str=None):
        """Mark Price and Funding Rate

        Args:
            symbol (str, optional): [Target symbol]. Defaults to None.

        Returns:
            [Response Object]: [PyNance Response Object]
        """
        endpoint = "https://fapi.binance.com/fapi/v1/premiumIndex"
        if symbol is None: data = self.client._get(endpoint, True)
        else: data = self.client._get(endpoint, True, data={'symbol': symbol})
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data