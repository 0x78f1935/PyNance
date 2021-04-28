class System(object):
    """Based on https://binance-docs.github.io/apidocs/spot/en/#system-status-system

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client
    
    def maintenance(self):
        """Checks if the API server is under maintenance.
            On Status code 200
            
            Returns
            -------
            dict:
                { 
                    "status": 0,              // 0: normal，1：system maintenance
                    "msg": "normal"           // normal|system maintenance
                }
        """
        endpoint = "/sapi/v1/system/status/"
        return self.client._get(endpoint, True)
    
    def user_data(self):
        endpoint = "/sapi/v1/capital/config/getall"
        return self.client._get(endpoint, True)
    
    def trading_status(self):
        endpoint = "/sapi/v1/account/apiTradingStatus"
        return self.client._get(endpoint, True)