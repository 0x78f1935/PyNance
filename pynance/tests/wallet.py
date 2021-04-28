from unittest import TestCase
from pynance import PyNance
import pathlib

class WalletTest(TestCase):
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

    def test_deposit_address(self):
        if self.USE_IN_UNITTEST == 1:
            deposit_address = self.pynance_prod.wallet.deposit_address()
            self.assertEqual(deposit_address.coin, 'BTC')
            self.assertTrue('address' in deposit_address.json.keys())
            self.assertTrue('tag' in deposit_address.json.keys())
            self.assertTrue('url' in deposit_address.json.keys())
