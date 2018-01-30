import requests
from core.feed_base import *

TEST_REST_URL = 'https://api-public.sandbox.gdax.com'
REST_URL = 'https://api.gdax.com'


class GDAXTrader(FeedBase):

    def __init__(self, coin=ETH, curr=USD):
        self.url = TEST_REST_URL
        self.coin = coin
        self.curr = curr
        self.coin_info = None

    def query_api(self, path):
        r = requests.get(self.url + path)
        if r.ok:
            return r.json()
        raise QueryException("Status Code: {}".format(r.status_code))

    def get_available_coins(self):
        return self.query_api('/products')

    def get_coin_info(self):
        if not self.coin_info:
            self.coin_info = self.query_api('/products/{}-{}'.format(self.coin, self.curr))
        return self.coin_info

    @property
    def stats(self):
        return self.query_api('/products/{}-{}/stats'.format(self.coin, self.curr))

    @property
    def value(self):
        return self.stats['last']

    @property
    def open(self):
        return self.stats['open']

    @property
    def high_24h(self):
        return self.stats['high']

    @property
    def low_24h(self):
        return self.stats['low']

    @property
    def volume(self):
        return self.stats['volume']

    @property
    def volume_30d(self):
        return self.stats['volume_30day']


class QueryException(Exception):
    pass

