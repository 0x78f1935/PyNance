
from pynance.core.response import Response
from pynance.core.exceptions import BinanceAPIException
from operator import itemgetter
import requests
import time
import hmac
import hashlib


class Core(object):
    def __init__(self, api_key, api_secret):
        self.endpoint = "https://www.binance.com"
        self._api_key = api_key
        self._api_secret = api_secret
        self.session = self._init_session()

        self.locked = False
        self.lockedTimeout = 0

    def _init_session(self):
        session = requests.session()
        session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'binance/PyNance',
            'X-MBX-APIKEY': self._api_key
        })
        return session

    def _objectify(self, response):
        return Response(response)
    
    def _handle_response(self):
        if self.response.status_code == 429:
            print(self.response.json())
            BinanceAPIException('You have been rate limited, stop making requests or your account might get banned', self.response.status_code)
        elif self.response.status_code == 418:
            print(self.response.json())
            BinanceAPIException('You have been temporarly banned, You made to many requests', self.response.status_code)
        elif self.response.status_code == 200:
            return self._objectify(self.response)
        else:
            print(self.response.json())
            BinanceAPIException('Unknown error', self.response.status_code)

    def _safeguard(self):
        if not self.locked: return True
        return False

    def _order_params(self, data):
        """Convert params to list with signature as last element
        :param data:
        :return:
        """
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _generate_signature(self, data):
        ordered_data = self._order_params(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(self._api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def _request(self, method, endpoint, signed=True, force_params=True, **kwargs):
        # Set timeout for the request
        kwargs['timeout'] = 10

        data = kwargs.get('data', None)
        # Check if the request contains data
        if data and isinstance(data, dict):
            kwargs['data'] = data

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

        if signed: # generate signature
            kwargs['data']['timestamp'] = int(time.time() * 1000)
            kwargs['data']['signature'] = self._generate_signature(kwargs['data'])
        
        # sort get and post params to match signature order
        if data:
            # sort post params
            kwargs['data'] = self._order_params(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del(kwargs['data'])

        self.response = getattr(self.session, method)(endpoint, **kwargs)
        return self._handle_response()
    
    def get(self, endpoint, signed=False, **kwargs):
        return self._request('get', endpoint, signed, **kwargs)
