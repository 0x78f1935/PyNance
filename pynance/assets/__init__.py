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