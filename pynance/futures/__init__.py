from pynance.futures.assets import Assets
from pynance.futures.orders import Orders
from pynance.futures.wallet import Wallet
from pynance.core.exceptions import PyNanceException

class Futures(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#change-log
    """
    def __init__(self, client):
        self.client = client
        extensions = [
            ('Assets', Assets),
            ('Orders', Orders),
            ('Wallet', Wallet),
        ]
        [setattr(self, i[0].lower(), i[1](self.client)) for i in extensions]
    
    def leverage_bracket(self, symbol:str=None):
        """Provides leverage information about the provided symbol.

        Args:
            symbol (str, optional): [If empty returns all leverage brackets]. Defaults to None.

        Returns:
            [Respone]: [PyNance Response object]
        """
        endpoint = "https://fapi.binance.com/fapi/v1/leverageBracket"
        if symbol is None: 
            data = self.client._get(endpoint, signed=True)
        else:
            data = self.client._get(endpoint, signed=True)
            raw = [i for i in data.json if i['symbol'] == symbol]
            if raw: data = data._update_data({'_data': raw})
        self.client.logger.info(f'Weight: {data.info["weight"]} / 1200')
        return data

    def change_leverage(self, symbol:str=None, leverage:int=None):
        """Change user's initial leverage of specific symbol market.

        Args:
            symbol ([string], required): [target symbol].
            leverage ([integer], required): [target initial leverage: int from 1 to 125].
        """
        endpoint = "https://fapi.binance.com/fapi/v1/leverage"
        if symbol is None: raise PyNanceException("Please provide a valid symbol")
        if leverage is None: raise PyNanceException("Provide a valid leverage")
        if leverage <= 0 or leverage >= 126: raise PyNanceException("Leverage not in allowed range")
        _filter = {"symbol":symbol, "leverage": leverage}
        data = self.client._post(endpoint, True, data=_filter)
        self.client.logger.info(f'Weight: {data.info["weight"]} / 1200')
        return data

    def change_margin_type(self, symbol:str=None, margin_type:str=None):
        """Change user's initial leverage of specific symbol market.

        Args:
            symbol ([string], required): [target symbol].
            margin_type ([string], required): [Type of margin; ISOLATED or CROSSED].
        """
        endpoint = "https://fapi.binance.com/fapi/v1/marginType"
        if symbol is None: raise PyNanceException("Please provide a valid symbol")
        if margin_type is None: raise PyNanceException("Provide a valid margin_type")
        if margin_type.upper() not in ['ISOLATED', 'CROSSED']: raise PyNanceException("Margin Type has to be ISOLATED or CROSSED")
        _filter = {"symbol":symbol, "marginType": margin_type.upper()}
        data = self.client._post(endpoint, True, data=_filter)
        self.client.logger.info(f'Weight: {data.info["weight"]} / 1200')
        return data