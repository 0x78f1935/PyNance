from unittest import TestSuite as BaseSuite
from unittest import TextTestRunner

from pynance.tests.system import SystemTest
from pynance.tests.history import HistoryTest
from pynance.tests.wallet import WalletTest

class TestSuite(BaseSuite):
    def __init__(self):
        BaseSuite.__init__(self)
        self._test_cases = {
            'test_system': SystemTest,
            'test_history': HistoryTest,
            'test_wallet': WalletTest
        }
        self._instantate()
    
    def _instantate(self):
        for key, value in self._test_cases.items():
            self.addTest(value(key))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(TestSuite())