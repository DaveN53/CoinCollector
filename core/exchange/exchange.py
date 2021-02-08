from typing import List

from core.enums import OrderAction


class Exchange:

    def __init__(self):
        self._last_sold = 0
        self._last_buy = 0

    @property
    def last_sold_price(self):
        return self._last_sold

    @property
    def last_buy_price(self):
        return self._last_buy

    def get_candles(self, coin_symbol: str, market_symbol: str):
        raise NotImplementedError

    def get_latest_coin_data(self, coin_symbol: str, market_symbol: str):
        """
        :param coin_symbol: Symbol of coin we're buying
        :param market_symbol: currency we're buying it in
        :return:
        """
        raise NotImplementedError

    def subscribe_ticker_channel(self, product_ids: List[str]):
        raise NotImplementedError
