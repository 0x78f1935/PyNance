class Wallet(object):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def balance(self, **params):
        data = self.client.get(f'{self.client.endpoint}/api/v3/account', signed=True, data=params)
        if data.isSucces: return data.json['balances']
        return []