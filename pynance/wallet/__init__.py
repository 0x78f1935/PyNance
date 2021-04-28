class Wallet(object):
    """Based on https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-user_data

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client
    
    def deposit_address(self, coin="BTC"):
        """Fetch deposit address with network.
            On Status code 200
            
            Returns
            -------
            dict:
                {
                    "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
                    "coin": "BTC",
                    "tag": "",
                    "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
                }
        """
        endpoint = "/sapi/v1/capital/deposit/address"
        return self.client._get(endpoint, True, data={'coin': coin})
