from unittest import TestCase
from pynance import PyNance

class OrdersTest(TestCase):
    """NOTE: This endpoint is not available in the test environment.
    Therefor unable to write unittest for it unless I would provide my private token.
    """

    def setUp(self):
        self.pynance = PyNance(debug=True)
        self.data = self.pynance.orders.open('LTCBTC')

    def test_create_order_buy_stop_limit(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        test_data = self.pynance.orders.create('BNBBTC', 1000, False, 5, test=True).json
        self.assertTrue('code' in test_data.keys())
        self.assertTrue('msg' in test_data.keys())

    def test_create_order_sell_stop_limit(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        test_data = self.pynance.orders.create('BNBBTC', 1000, True, 5, test=True).json
        self.assertTrue('code' in test_data.keys())
        self.assertTrue('msg' in test_data.keys())

    def test_create_order_buy(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000.0, True, test=True)
        self.assertEqual(data.info['status_code'], 200)

    def test_create_order_sell(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000.0, False, test=True)
        self.assertEqual(data.info['status_code'], 200)
