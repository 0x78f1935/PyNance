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