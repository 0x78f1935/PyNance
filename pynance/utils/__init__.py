from datetime import datetime

class Utils(object):
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    def servertime(self, to_date=False, strftime=None):
        """Get the current Binance server time

        Args:
            to_date (bool, optional): Formats the date with the datetime library. Defaults to False.
            strftime (string, optional): Use strformat string format to manipulate the date. Defaults to None.

        Returns:
            str: The Binance server time formatted according to the options
        """
        response = self.client.get(f'{self.client.endpoint}/api/v3/time', signed=False)
        if to_date or strftime is not None: 
            if strftime is not None:
                return str(datetime.utcfromtimestamp(response.json['serverTime']/1000).strftime(strftime))
            else: return str(datetime.utcfromtimestamp(response.json['serverTime']/1000))
        else: return str(response.json['serverTime'])
