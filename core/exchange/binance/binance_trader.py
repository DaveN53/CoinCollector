import requests
from binance.client import Client

from core.exchange.exchange import Exchange


class BinanceTrader(Exchange):

    def __init__(self, api_key, api_secret, market_coin='ETH'):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.market_coin = market_coin

    def get_last_bid(self, coin='BNB'):
        orders = self.get_order_book(coin=coin)
        bids = orders['bids']
        price = bids[0][0]
        quantity = bids[0][1]
        return price

    def get_order_book(self, coin='BNB'):
        """
        symbol='BNBETH'
        :param coin: Coin to exchange for market coin
        :return:
        """
        symbol = coin + self.market_coin
        print(symbol)
        result = self.client.get_order_book(symbol=symbol)
        return result

    def get_symbol_info(self, coin='BNB'):
        """
        :param coin:
        :return:
        """
        symbol = coin + self.market_coin
        result = self.client.get_symbol_info(symbol=symbol)
        return result

    def get_price_info(self, coin='BNB'):
        result = self.get_symbol_info(coin=coin)
        filters = result['filters'][0]
        price = {
            'min': filters['minPrice'],
            'max': filters['maxPrice']
        }
        return price

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError