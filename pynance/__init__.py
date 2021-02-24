from pynance.core import Core
from pynance.wallet import Wallet
from pynance.price import Price
from pynance.orders import Orders
from datetime import datetime


class PyNance(Core):
    def __init__(self, api_key, api_secret, endpoint="https://www.binance.com", app=None):
        self.endpoint = endpoint # Needs to be before super of Core
        Core.__init__(self, api_key, api_secret, app)
        self.wallet = Wallet(self)
        self.price = Price(self)
        self.orders = Orders(self)

    def servertime(self, to_date=False, strftime=None):
        """Get the current Binance server time

        Args:
            to_date (bool, optional): Formats the date with the datetime library. Defaults to False.
            strftime (string, optional): Use strformat string format to manipulate the date. Defaults to None.

        Returns:
            str: The Binance server time formatted according to the options
        """
        response = self.get(f'{self.endpoint}/api/v3/time', signed=False)
        if to_date or strftime is not None: 
            if strftime is not None: return str(
                datetime.utcfromtimestamp(response.json['serverTime']/1000).strftime(strftime)
            )
            else: return str(datetime.utcfromtimestamp(response.json['serverTime']/1000))
        else: return str(response.json['serverTime'])
