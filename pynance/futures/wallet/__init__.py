class Wallet(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-v2-user_data

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client

    def balance(self):
        endpoint = "https://fapi.binance.com/fapi/v2/balance"
        data = self.client._get(endpoint, True)
        self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
        return data