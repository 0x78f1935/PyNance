from pynance.core.exceptions import PyNanceException
from pynance.core import Core
import logging

from pynance.system import System
from pynance.history import History
from pynance.wallet import Wallet
from pynance.assets import Assets
from pynance.orders import Orders

class PyNance(Core):
    def __init__(self, api_key=None, api_secret=None, flask_app=False, debug=False, verbose=False):
        """Call this class to instantiate PyNance.        

        Args:
            api_key (str, required): [Binance API key, required unless debug is True]
            api_secret (str, required): [Binance API secret, required unless debug is True]
            flask_app (bool, optional): [Defaults to false, when true. Skip Instantiate credentials so we can call it through flask.]
            debug (bool, optional): [Defaults to False When True connect to the Binance Test Sandbox environment".]

        """
        if debug:
            api_key = "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca"
            api_secret = "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD"
            api_endpoint = "https://testnet.binance.vision"
        else:
            if (api_key is None or api_secret is None) and not flask_app: raise PyNanceException("Please provide an valid  api_key and api_secret")
            api_endpoint="https://api.binance.com"
        Core.__init__(self, api_key, api_secret, api_endpoint, verbose)

        if not flask_app: self._set_session_headers()

        self.logger.debug(f'Loading all available modules ...')
        extensions = [
            ('System', System),
            ('History', History),
            ('Wallet', Wallet),
            ('Assets', Assets),
            ('Orders', Orders)
        ]
        [setattr(self, i[0].lower(), i[1](self)) for i in extensions]
        self.logger.info(f'PyNance Ready for use ...')

    def init_app(self, app):
        """This method can be used to instantiate a instance in a flask application.
        This flask configuration needs to contain the following variables linked to your binance
        information

        - BINANCE_API_KEY
        - BINANCE_API_SECRET
        - BINANCE_API_ENDPOINT
        """
        self.logger.debug(f'PyNance found a Flask app, loading credentials from flask configuration ...')
        self.api_key = app.config["BINANCE_API_KEY"]
        self.api_secret = app.config["BINANCE_API_SECRET"]
        self.api_endpoint = app.config['BINANCE_API_ENDPOINT']
        self.logger.debug(f'Flask configuration loaded ...')
        self._set_session_headers()
