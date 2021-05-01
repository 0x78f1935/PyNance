from unittest import TestCase
from pynance import PyNance
import pathlib

class AssetsTest(TestCase):
    def setUp(self):
        self.USE_IN_UNITTEST = None
        self.API_KEY = None
        self.API_SECRET = None

        # Open environment file to check with production credentials
        env_file = pathlib.Path(pathlib.PurePosixPath(pathlib.Path(__file__).resolve().parent.parent.parent, '.env'))
        if env_file.is_file():
            with open(env_file, 'r') as f:
                for line in f.readlines():
                    key, value = line.split('=')
                    setattr(self, key, value.replace('\n', ''))
            if self.USE_IN_UNITTEST is not None: self.USE_IN_UNITTEST = int(self.USE_IN_UNITTEST)
        # Set prod and dev env 
        if self.USE_IN_UNITTEST == 1: 
            self.pynance_prod = PyNance(api_key=self.API_KEY, api_secret=self.API_SECRET)
        self.pynance_test = PyNance(debug=True)

    def test_asset_details(self):
        if self.USE_IN_UNITTEST == 1: 
            test_data = self.pynance_prod.assets.details().json
            self.assertIsInstance(test_data['BTC'], dict)
            self.assertTrue('withdrawFee' in test_data['BTC'])
            self.assertTrue('minWithdrawAmount' in test_data['BTC'])
            self.assertTrue('withdrawStatus' in test_data['BTC'])
            self.assertTrue('depositStatus' in test_data['BTC'])

    def test_asset_fees(self):
        if self.USE_IN_UNITTEST == 1: 
            self.assertGreaterEqual(len(self.pynance_prod.assets.fees().json), 1)

    def test_average(self):
        test_data = self.pynance_test.assets.average('LTCBTC')
        self.assertIsInstance(test_data, float)

    def test_symbols(self):
        test_data = self.pynance_test.assets.symbols('LTCBTC')
        self.assertTrue('symbol' in test_data.json)
        self.assertTrue('price' in test_data.json)
        self.assertEqual(test_data.json['symbol'], 'LTCBTC')
        self.assertEqual(test_data.json['price'], '0.01100000')
    
    def test_klines(self):
        test_data = self.pynance_test.assets.klines('LTCBTC')
        self.assertGreaterEqual(len(test_data), 1)
        test_data = self.pynance_test.assets.klines('LTCBTC', "15m", 1)
        self.assertEqual(len(test_data), 1)
