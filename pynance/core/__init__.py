from pynance.core.response import Response
from pynance.core.exceptions import *
from operator import itemgetter
import requests
import hashlib
import logging
import time
import hmac

class Core(requests.Session):
    def __init__(self, api_key, api_secret, api_endpoint, verbose=False):
        requests.Session.__init__(self)
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_endpoint = api_endpoint

        logging.basicConfig(
            format='%(asctime)s [PyNance:%(levelname)s](%(funcName)s:%(lineno)d) -> %(message)s', 
            datefmt='%I:%M:%S %p %d-%m-%Y', 
            level=logging.DEBUG if verbose else logging.INFO
        )
        self.logger = logging.getLogger('PyNance')
        self.logger.debug('Core instantiated ...')

    def _set_session_headers(self):
        """Sets the headers to make requests with the binance API based on the provided token information"""
        self.logger.debug('Set request headers ...')
        self.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'binance/PyNance',
            'X-MBX-APIKEY': self.api_key
        })
        self.logger.debug('API-Key ready ...')

    def _request(self, method, endpoint, authenticated=True, force_params=False, timeout=10, **kwargs):
        """[summary]

        Args:
            method (string, required): [The request method, GET, POST, etc]
            endpoint (string, required): [The endpoint]
            authenticated (bool, optional): [Authenticated request]. Defaults to True.
            request_params ([tuple], optional): [When set, force the parameters in the endpoint as args].
            timeout (int, optional): [The time in seconds until the request will timeout]. Defaults to 10.
        """
        if 'binance.com' not in endpoint: 
            self.logger.warning(f'Endpoint seems to be without base url ... {endpoint} ... applying base url ...')
            endpoint = self.api_endpoint + endpoint

        self.logger.debug(f'Processing request data for ... {endpoint} ...')
        data = kwargs.get('data', {})
        kwargs['data'] = data
        # Check if the request contains data
        if data and isinstance(data, dict):

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

        if authenticated: # generate signature
            self.logger.debug(f'Signing ... {endpoint} ...')
            kwargs['data']['timestamp'] = int(time.time() * 1000)
            kwargs['data']['signature'] = self._sign(kwargs['data'])
        
        # sort get and post params to match signature order
        if data:
            # sort post params
            kwargs['data'] = self._order(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del(kwargs['data'])

        response = getattr(self, method)(endpoint, **kwargs)

        if 'x-mbx-used-weight' in response.headers.keys(): 
            self.logger.debug(f'Weight: {response.headers["x-mbx-used-weight"]} kg')

        return self._handle_response(response)

    def _sign(self, data:dict):
        """Signs the request with the authentication information provided by the enduser."""
        ordered_data = self._order(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data]).encode('utf-8')
        m = hmac.new(self.api_secret.encode('utf-8'), query_string, hashlib.sha256)
        return m.hexdigest()

    def _order(self, data:dict):
        """Orders the data so Binance accepts the request"""
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

    def _handle_response(self, resp):
        resp = Response(resp)
        self.close() # Close the response
        self.logger.info(f'Request ... {resp.response_info["endpoint"]} ... Done with status code {resp.response_info["status_code"]}!')
        return resp

    def _get(self, endpoint, signed=False, **kwargs):
        """Executes a get request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.get(
                f'{client.endpoint}/api/v3/klines', 
                signed=False, 
                data={"symbol": "LTCBTC", "interval": "1m"}
            )
        """
        self.logger.debug(f'GET request for ... {endpoint} ...')
        return self._request('get', endpoint, signed, **kwargs)
    
    def _post(self, endpoint, signed=False, **kwargs):
        """Executes a post request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.post(
                f'{client.endpoint}/api/v3/order', 
                signed=False, 
                data={"symbol": "LTC", "quantity": "1"}
            )
        """
        self.logger.debug(f'POST request for ... {endpoint} ...')
        return self._request('post', endpoint, signed, **kwargs)

    def _delete(self, endpoint, signed=False, **kwargs):
        """Executes a delete request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.delete(
                f'{client.endpoint}/api/v3/order', 
                signed=False, 
                data={"symbol": "LTC", "origClientOrderId": "1"}
            )
        """
        self.logger.debug(f'DELETE request for ... {endpoint} ...')
        return self._request('delete', endpoint, signed, **kwargs)
