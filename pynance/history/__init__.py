class History(object):
    """Based on https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client
    
    def deposit(self):
        """Fetch deposit history.
            On Status code 200
            
            Returns
            -------
            list:
                [
                    {
                        "amount":"0.00999800",
                        "coin":"PAXG",
                        "network":"ETH",
                        "status":1,
                        "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
                        "addressTag":"",
                        "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
                        "insertTime":1599621997000,
                        "transferType":0,
                        "confirmTimes":"12/12"
                    }, ...
                ]
        """
        endpoint = "/sapi/v1/capital/deposit/hisrec"
        data = self.client._get(endpoint, True)
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data

    def withdraw(self):
        """Fetch withdraw history.
            On Status code 200
            
            Returns
            -------
            list:
                [
                    {
                        "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
                        "amount": "8.91000000",
                        "applyTime": "2019-10-12 11:12:02",
                        "coin": "USDT",
                        "id": "b6ae22b3aa844210a7041aee7589627c",
                        "withdrawOrderId": "WITHDRAWtest123", // will not be returned if there's no withdrawOrderId for this withdraw.
                        "network": "ETH", 
                        "transferType": 0,   // 1 for internal transfer, 0 for external transfer   
                        "status": 6,
                        "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"
                    }, ...
                ]
        """
        endpoint = "/sapi/v1/capital/withdraw/history"
        data = self.client._get(endpoint, True)
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data
