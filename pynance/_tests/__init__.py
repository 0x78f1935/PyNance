from unittest import TestSuite as BaseSuite
from unittest import TextTestRunner

from pynance._tests.system import SystemTest
from pynance._tests.history import HistoryTest
from pynance._tests.wallet import WalletTest
from pynance._tests.assets import AssetsTest
from pynance._tests.orders import OrdersTest
from pynance._tests.futures import FuturesTest

class TestSuite(BaseSuite):
    def __init__(self):
        BaseSuite.__init__(self)
        self._test_cases = {
            'test_system': SystemTest,
            'test_history': HistoryTest,
            'test_wallet': WalletTest,
            'test_assets': AssetsTest,
            'test_orders': OrdersTest,
            'test_futures': FuturesTest
        }
        self._instantate()
    
    def _instantate(self):
        for key, value in self._test_cases.items():
            self.addTest(value(key))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(TestSuite())