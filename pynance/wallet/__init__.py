class Wallet(object):
    def __init__(self, client):
        self.client = client

    def balance(self):
        data = self.client.get(f'{self.client.endpoint}/api/v3/account', signed=True, data={})
        if data.isSucces: return data.json['balances']
        return []