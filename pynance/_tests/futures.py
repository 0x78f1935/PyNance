from unittest import TestCase
from pynance import PyNance
import pathlib

class FuturesTest(TestCase):
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

    
    def test_exchange_info(self):
        test_data = self.pynance_test.futures.assets.exchange_info(['LTCBTC'])
        self.assertTrue('timezone' in test_data.json.keys())
        self.assertTrue('serverTime' in test_data.json.keys())
        self.assertTrue('futuresType' in test_data.json.keys())
        self.assertTrue('rateLimits' in test_data.json.keys())
        self.assertTrue('exchangeFilters' in test_data.json.keys())
        self.assertTrue('assets' in test_data.json.keys())
        self.assertTrue('symbols' in test_data.json.keys())
        
        self.assertEqual(type(test_data.json['timezone']), str)
        self.assertEqual(type(test_data.json['serverTime']), int)
        self.assertEqual(type(test_data.json['futuresType']), str)
        self.assertEqual(type(test_data.json['rateLimits']), list)
        self.assertEqual(type(test_data.json['exchangeFilters']), list)
        self.assertEqual(type(test_data.json['assets']), list)
        self.assertEqual(type(test_data.json['symbols']), list)
    
    def test_leverage_brackets(self):
        if self.USE_IN_UNITTEST == 1: 
            leverage_bracket = self.pynance_prod.futures.leverage_bracket()
            self.assertGreaterEqual(len(leverage_bracket.json), 5)
            leverage_bracket = self.pynance_prod.futures.leverage_bracket('LTCUSDT')
            self.assertEqual(len(leverage_bracket.json), 1)
