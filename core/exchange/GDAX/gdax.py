import enum
import json
from contextlib import contextmanager
from typing import List, Callable

import requests
from requests import Response
from websocket import WebSocketApp

TEST_REST_URL = 'https://api-public.sandbox.pro.coinbase.com'
REST_URL = 'https://api.pro.coinbase.com'
WEBSOCKET_URL = 'wss://ws-feed.pro.coinbase.com'


class ReturnCode(enum.Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNARL_SERVER_ERROR = 500


class GDAXApi:
    def __init__(self):
        self.base_url = REST_URL


class MarketDataApi(GDAXApi):

    def __init__(self):
        super().__init__()
        self.url = self.base_url + '/products'

    @staticmethod
    def handle_response(response: Response):
        return json.loads(response.content)

    def get_product(self):
        """
        Get a list of available currency pairs for trading.
        https://docs.pro.coinbase.com/#get-products
        :return:
        """
        return self.handle_response(requests.get(self.url))

    def get_single_product(self, coin_symbol: str, market_symbol: str):
        """
        Get market data for a specific currency pair.
        https://docs.pro.coinbase.com/#get-single-product
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}'
        return self.handle_response(requests.get(request_url))

    def get_product_order_book(self, coin_symbol: str, market_symbol: str, level: int = None):
        """
        Get a list of open orders for a product. The amount of detail shown can be customized with the level parameter.
        https://docs.pro.coinbase.com/#get-product-order-book
        :param coin_symbol:
        :param market_symbol:
        :param level:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}/book'
        if level:
            request_url += f'?={level}'

        return self.handle_response(requests.get(request_url))

    def get_product_ticker(self, coin_symbol: str, market_symbol: str):
        """
        Snapshot information about the last trade (tick), best bid/ask and 24h volume.
        https://docs.pro.coinbase.com/#get-product-ticker
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}/ticker'
        return self.handle_response(requests.get(request_url))

    def get_trades(self, coin_symbol: str, market_symbol: str):
        """
        List the latest trades for a product.
        https://docs.pro.coinbase.com/#get-trades
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}/trades'
        return self.handle_response(requests.get(request_url))

    def get_candles(self, coin_symbol: str, market_symbol: str, granularity: int = 60):
        return self.get_historic_rates(coin_symbol, market_symbol, granularity)

    def get_historic_rates(self, coin_symbol: str, market_symbol: str, granularity: int = 60):
        """
        Historic rates for a product. Rates are returned in grouped buckets based on requested granularity.
        https://docs.pro.coinbase.com/#get-historic-rates
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}/candles?granularity={granularity}'
        return self.handle_response(requests.get(request_url))

    def get_24hr_stats(self, coin_symbol: str, market_symbol: str):
        """
        Get 24 hr stats for the product. volume is in base currency units. open, high, low are in quote currency units.
        https://docs.pro.coinbase.com/#get-24hr-stats
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        request_url = f'{self.url}/{coin_symbol}-{market_symbol}/stats'
        return self.handle_response(requests.get(request_url))

    def get_currencies(self):
        """
        List known currencies.
        https://docs.pro.coinbase.com/#get-currencies
        :return:
        """
        request_url = f'{self.base_url}/currencies'
        return self.handle_response(requests.get(request_url))

    def get_currency(self, symbol: str):
        """
        List the currency for specified id.
        https://docs.pro.coinbase.com/#get-a-currency
        :param symbol:
        :return:
        """
        request_url = f'{self.base_url}/currencies/{symbol}'
        return self.handle_response(requests.get(request_url))

    def get_time(self):
        """
        Get the API server time.
        https://docs.pro.coinbase.com/#time
        :return:
        """
        request_url = f'{self.base_url}/time'
        return self.handle_response(requests.get(request_url))


class GDAXWebsocket:
    """
    Stream product data
    Store in memory until time frame met then write to DB
    """
    def __init__(self):
        self.__ws = None

    @staticmethod
    def __handle_error(ws, error):
        print(f'WS Error: {error}')

    def __open_websocket(self, subscribe_data: dict, process_data_func: Callable):
        """

        :param subscribe_data: Channel subscribe data
        :param process_data_func: function that takes two arguments (ws, message)
        :return:
        """

        def __on_open(ws):
            ws.send(data=json.dumps(subscribe_data))

        self.__ws = WebSocketApp(WEBSOCKET_URL, on_message=process_data_func, on_error=self.__handle_error)
        self.__ws.on_open = __on_open
        self.__ws.run_forever()

    def close_websocket(self):
        self.__ws.close()

    def ticker_channel_socket(self, process_data_func: Callable, product_ids = List[str]):
        """
        Example Response
        [{
            "type": "ticker",
            "trade_id": 20153558,
            "sequence": 3262786978,
            "time": "2017-09-02T17:05:49.250000Z",
            "product_id": "BTC-USD",
            "price": "4388.01000000",
            "side": "buy", // Taker side
            "last_size": "0.03000000",
            "best_bid": "4388",
            "best_ask": "4388.01"
        },]
        :param process_data_func: function to process data on socket receive
        :param product_ids: List of string product ids: ['ETH-USD', 'ETH-BTC']
        :return:
        """
        print('Creating Socket')
        subscribe_data = {
            'type': 'subscribe',
            'product_ids': product_ids,
            'channels': [{'name': 'ticker', 'product_ids': product_ids}]
        }
        self.__open_websocket(subscribe_data, process_data_func=process_data_func)
        return self.__ws

