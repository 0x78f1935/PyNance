class BinanceAPIException(Exception):

    def __init__(self, msg, status_code):
        self.status_code = status_code
        self.msg = msg

    def __str__(self):  # pragma: no cover
        return f'APIError(code={self.status_code}): {self.msg}'
