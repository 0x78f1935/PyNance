from unittest import TestCase
from pynance import PyNance
import pathlib

class SystemTest(TestCase):
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

    
    def test_maintenance(self):
        """Not available in test environment"""
        if self.USE_IN_UNITTEST == 1:
            maintenance = self.pynance_prod.system.maintenance()
            self.assertTrue(maintenance.json['status'] <= 1)
            self.assertTrue(maintenance.json['status'] >= 0)
            self.assertTrue(maintenance.json['msg'], True if maintenance.json['msg'] in 'normal|system' else False)
    
    def test_user_data(self):
        """Only works when there is value in the account.
        """
        if self.USE_IN_UNITTEST == 1:
            self.assertGreaterEqual(len(self.pynance_prod.system.user_data().json), 1)

    def test_trading_status(self):
        """Only works when there is value in the account.
        """
        if self.USE_IN_UNITTEST == 1:
            test_data = self.pynance_prod.system.trading_status().json
            self.assertIsInstance(test_data['data'], dict)
            self.assertTrue('isLocked' in test_data['data'].keys())
            self.assertTrue('plannedRecoverTime' in test_data['data'].keys())
            self.assertTrue('triggerCondition' in test_data['data'].keys())
            self.assertTrue('indicators' in test_data['data'].keys())
            self.assertTrue('updateTime' in test_data['data'].keys())
            self.assertGreaterEqual(len(self.pynance_prod.system.trading_status().json), 1)