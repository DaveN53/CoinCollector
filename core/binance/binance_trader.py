import requests
from binance.client import Client

class BinanceTrader:

    def __int__(self, api_key, api_secret):
        self.client = Client(api_key=api_key, api_secret=api_secret)

    def get_exchange_rate(self, buy_coin, sell_coin):
        """
        symbol='BNBBTC'
        :param buy_coin:
        :param sell_coin:
        :return:
        """
        symbol = buy_coin + sell_coin
        result = self.client.get_order_book(symbol=symbol)
        return result

    def get_buy_rate(self, buy_coin, sell_coin='BNB'):
        """
        Trade buy coin for sell coin(BNB)
        :param buy_coin:
        :param sell_coin:
        :return:
        """
        return self.get_exchange_rate(buy_coin=buy_coin, sell_coin=sell_coin)

    def get_sell_rate(self,  sell_coin, buy_coin='BNB'):
        """
        Trade sell coin for buy coin(BNB)
        :param sell_coin:
        :param buy_coin:
        :return:
        """
        return self.get_exchange_rate(buy_coin=buy_coin, sell_coin=sell_coin)

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError