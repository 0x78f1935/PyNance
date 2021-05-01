from pynance.core.exceptions import BinanceAPIException
from statistics import mean


class Assets(object):
    """
    Based on https://binance-docs.github.io/apidocs/spot/en/#asset-detail-user_data

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
        endpoint = "/api/v3/ticker/price"
        if symbol is None: return self.client._get(endpoint, False)
        else: return self.client._get(endpoint, False, data={'symbol': symbol})
    
    def details(self, asset="BTC"):
        """Fetch details of assets supported on Binance.
            On Status code 200
            
            Returns
            -------
            list:
                [
                    "CTR": {
                        "minWithdrawAmount": "70.00000000", //min withdraw amount
                        "depositStatus": false,//deposit status (false if ALL of networks' are false)
                        "withdrawFee": 35, // withdraw fee
                        "withdrawStatus": true, //withdraw status (false if ALL of networks' are false)
                        "depositTip": "Delisted, Deposit Suspended" //reason
                    }, ...
                ]
        """
        endpoint = "/sapi/v1/asset/assetDetail"
        return self.client._get(endpoint, True, data={'asset': asset})

    def fees(self, symbol="BTCUSDT"):
        """Fetch details of assets supported on Binance.
            On Status code 200
            
            Returns
            -------
            list:
                [
                    {
                        "symbol": "ADABNB",
                        "makerCommission": "0.001",
                        "takerCommission": "0.001"
                    }, ...
                ]
        """
        endpoint = "/sapi/v1/asset/tradeFee"
        return self.client._get(endpoint, True, data={'symbol': symbol})

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
        endpoint = "/api/v3/klines"
        if timeframe is None: timeframe = "1m"
        if timeframe not in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']: 
            raise BinanceAPIException("Timeframe is unknown, use one of the following timeframes: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']")
        data = [{
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
        } for i in self.client._get(
            endpoint,
            False, 
            data={
                "symbol": asset,
                "interval": timeframe,
                "limit": total_candles
            }
        ).json]
        if low: return mean([float(i["low"]) for i in data])
        else: return mean([float(i["high"]) for i in data])
    
    def klines(self, symbol="LTCBTC", timeframe="1h", total_candles=500):
        """Returns information based on the provided symbol
        
        Args:
            symbol (str, optional): [Symbol]. Defaults to "LTCBTC".
            timeframe (str, optional): [timeframe which is also available in binance graphs]. Defaults to "1h".
            total_candles (int, optional): [total amount of candles to return]. Defaults to 500.

        Returns:
            [list]: [The list can be used in candle charts for example]

            [
                [
                    1499040000000,      // Open time
                    "0.01634790",       // Open
                    "0.80000000",       // High
                    "0.01575800",       // Low
                    "0.01577100",       // Close
                    "148976.11427815",  // Volume
                    1499644799999,      // Close time
                    "2434.19055334",    // Quote asset volume
                    308,                // Number of trades
                    "1756.87402397",    // Taker buy base asset volume
                    "28.46694368",      // Taker buy quote asset volume
                    "17928899.62484339" // Ignore.
                ]
            ]
        """
        endpoint = "/api/v3/klines"
        return self.client._get(
            endpoint,
            False, 
            data={
                "symbol": symbol,
                "interval": timeframe,
                "limit": total_candles,
            }
        ).json