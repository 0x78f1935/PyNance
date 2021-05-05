from pynance.futures.assets import Assets

class Futures(object):
    def __init__(self, client):
        self.client = client
        extensions = [
            ('Assets', Assets)
        ]
        [setattr(self, i[0].lower(), i[1](self.client)) for i in extensions]
    
    def leverage_bracket(self, symbol:str=None):
        endpoint = "https://fapi.binance.com/fapi/v1/leverageBracket"
        if symbol is None: 
            data = self.client._get(endpoint, signed=True)
        else:
            data = self.client._get(endpoint, signed=True)
            raw = [i for i in data.json if i['symbol'] == symbol]
            if raw: data = data._update_data({'_data': raw})
        self.client.logger.info(f'Weight: {data.info["weight"]} / 1200')
        return data
