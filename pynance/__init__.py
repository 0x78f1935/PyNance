from pynance.core import Core as _Core
from pynance.utils import Utils as _Utils
from pynance.orders import Orders as _Orders
from pynance.wallet import Wallet as _Wallet

class Client(_Core):
    def __init__(self, api_key, api_secret):
        _Core.__init__(self, api_key, api_secret)
        self.utils = _Utils(self)
        self.orders = _Orders(self)
        self.wallet = _Wallet(self)

    def test(self):
        print(self.utils.servertime(True))
        open_orders = self.orders.open_orders()
        print(open_orders)

        test = self.wallet.balance()
        print(test)
