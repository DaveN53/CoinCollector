import requests
from core.feed_base import *

TEST_REST_URL = 'https://api-public.sandbox.gdax.com'
REST_URL = 'https://api.gdax.com'
WEBSOCKET_URL = 'wss://ws-feed-public.sandbox.gdax.com'


class GDAXFeedManager(FeedBase):

    def __init__(self):
        self.url = TEST_REST_URL

    def query_api(self, path):
        r = requests.get(self.url + '/products')

        return r.json

    def get_coins(self):
        return self.query_api('/products')

    def get_value(self, coin=ETH, curr=USD):
        coins_json = self.get_coins()
        