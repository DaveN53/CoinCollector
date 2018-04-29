import requests
import logging
from core.enums import Currencies, OrderAction

TEST_REST_URL = 'https://api-public.sandbox.gdax.com'
REST_URL = 'https://api.gdax.com'


class GDAXTrader():

    def __init__(self,
                 coin: Currencies=Currencies.ETH,
                 curr: Currencies=Currencies.USD,
                 last_sold: int = 0,
                 last_buy: int = 0):
        self.url = REST_URL
        self.coin = coin
        self.curr = curr
        self.last_sold = last_sold
        self.last_buy = last_buy
        self.coin_info = None

    def query_api(self, path, params=None):
        r = requests.get(self.url + path, params=params)
        if r.ok:
            return r.json()
        raise QueryException("Status Code: {}".format(r.status_code))

    def create_limit_order(self, current_price: float, action: OrderAction):

        return

    def create_stop_limit_order(self, current_price: float, action: OrderAction):
        """
        Stop is when the order is placed with the value of limit
        :param current_price:
        :param action:
        :return:
        """
        limit = 0
        stop = 0
        return


    def get_available_coins(self):
        return self.query_api('/products')

    def get_coin_info(self):
        if not self.coin_info:
            self.coin_info = self.query_api('/products/{}-{}'.format(self.coin, self.curr))
        return self.coin_info

    @property
    def order_book(self):
        response = self.query_api(
            path='/products/{}-{}/book'.format(self.coin, self.curr),
            params={'level': 2}
        )
        return response

    @property
    def ticker(self):
        response = self.query_api('/products/{}-{}/ticker'.format(self.coin, self.curr))
        if 'message' in response:
            logging.info('{} : {} : {}'.format(self.coin, self.curr, response['message']))
        return response

    @property
    def stats(self):
        return self.query_api('/products/{}-{}/stats'.format(self.coin, self.curr))

    @property
    def last_sold_price(self):
        return self.last_sold

    @property
    def price(self):
        return float(self.ticker['price'])

    @property
    def last(self):
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

