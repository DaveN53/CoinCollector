from datetime import datetime

from core.exchange.GDAX.gdax import MarketDataApi
from core.exchange.exchange import Exchange


class GDAXTrader(Exchange):

    def __init__(self):
        super().__init__()
        self._market_data_api = MarketDataApi()
        self.last_volume = None

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
            "price": float(response['price']),
            "volume": self.calculate_ticker_volume(float(response['volume']))
        }

    def calculate_ticker_volume(self, volume_24h: float) -> float:
        """
        Calculate 1 min volume by find the difference between the currently reported volume and the last volume
        If no last volume is available calculate volume by dividing 24h volume by number of minutes that have
        passed in the day as a best effort
        :param volume_24h:
        :return:
        """
        now = datetime.now()
        min_since_last_hour = (now - now.replace(minute=0, second=0, microsecond=0)).total_seconds() / 60

        if min_since_last_hour < 1:
            return volume_24h / (24*60)

        if not self.last_volume:
            self.last_volume = volume_24h
            return volume_24h / (24*60)

        print(f'Last Volume: {self.last_volume} Current Volume:{volume_24h}')

        last_volume = self.last_volume
        self.last_volume = volume_24h
        min_volume = volume_24h - last_volume
        print(f'Minute Volume: {min_volume}')
        return min_volume

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



