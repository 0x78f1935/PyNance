from json import JSONDecodeError

class Response(object):
    def __init__(self, response):
        self.response_info = {
            'status_code': response.status_code,
            'reason': response.reason,
            'weight': response.headers['x-mbx-used-weight'] if 'x-mbx-used-weight' in response.headers.keys() else 0,
            'endpoint': response.url.split('?').pop(0),
            'method': response.request.method
        }
        # Extend reason message based on response status code
        if response.status_code == 403: self.response_info['reason'] += ', HTTP 403 return code is used when the WAF Limit (Web Application Firewall) has been violated.'
        elif response.status_code == 429: self.response_info['reason'] += ', HTTP 429 return code is used when breaking a request rate limit.'
        elif response.status_code == 418: self.response_info['reason'] += ', HTTP 418 return code is used when an IP has been auto-banned for continuing to send requests after receiving 429 codes.'
        elif response.status_code >= 400 and response.status_code <= 499: self.response_info['reason'] += ', HTTP 4XX return codes are used for malformed requests; the issue is on the sender\'s side.'
        elif response.status_code >= 500 and response.status_code <= 599: self.response_info['reason'] += ', HTTP 5XX return codes are used for internal errors; the issue is on Binance\'s side.'

        try: self._data = response.json()
        except JSONDecodeError: self._data = []

        if isinstance(self._data, dict): [setattr(self, k, self._data[k]) for k in self._data.keys()]

    def _update_data(self, data:dict):
        for key, value in data.items():
            try:
                getattr(self, key)
                setattr(self, key, value)
            except AttributeError: pass
        return self

    @property
    def json(self):
        """Gets the RAW data from the response

        Returns:
            json type: Content directly from the Binance API
        """
        return self._data if self._data else []
    
    @property
    def info(self):
        """The response itself contains useful information, this method returns this info.

        Returns:
            Dict: Contains response values
                - status_code -> response status code
                - reason -> reasoning for the recieved status code
                - weight -> A heavier load request will weight more, to heavy will rate limit your requests
                - endpoint -> The endpoint that had been called to retrieve this response
                - method -> The method used to call the endpoint
        """
        return self.response_info
