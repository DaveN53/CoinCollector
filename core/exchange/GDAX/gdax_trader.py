from core.exchange.GDAX.gdax import MarketDataApi
from core.exchange.exchange import Exchange


class GDAXTrader(Exchange):

    def __init__(self):
        super().__init__()
        self._market_data_api = MarketDataApi()

    def get_latest_coin_data(self,coin_symbol: str, market_symbol: str):
        """
        :param coin_symbol: Symbol of coin we're buying
        :param market_symbol: currency we're buying it in
        :return:
        """
        response = self._market_data_api.get_product_ticker(coin_symbol, market_symbol)
        return {
            "coin_symbol": coin_symbol,
            "market_symbol": market_symbol,
            "price": float(response['price'])
        }

    def get_available_coins(self):
        return self._market_data_api.get_product()

    def get_coin_info(self, coin_symbol: str, market_symbol: str):
        return self._market_data_api.get_single_product(coin_symbol, market_symbol)

    def get_candles(self, coin_symbol: str, market_symbol: str):
        """
        [
            [ time, low, high, open, close, volume ],
            [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3 ]
        ]
        :return:
        """
        return self._market_data_api.get_candles(coin_symbol, market_symbol)

    def get_order_book(self, coin_symbol: str, market_symbol: str):
        return self._market_data_api.get_product_order_book(coin_symbol, market_symbol)



