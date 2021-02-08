import json
from datetime import datetime, timedelta, timezone
from threading import Thread
from typing import List

from core.database.db_helper import DBHelper
from core.exchange.GDAX.gdax import MarketDataApi, GDAXWebsocket
from core.exchange.exchange import Exchange


class GDAXTrader(Exchange):

    def __init__(self, db_helper: DBHelper):
        super().__init__()
        self._db_helper = db_helper
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
        print(f'{datetime.now()} Minute Volume: {min_volume}')
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

    def subscribe_ticker_channel(self, product_ids: List[str]):
        """
        Subscribes to ticker socket and stores data in database at interval
        :param product_ids: List str product ids [ETH-USD, ETH-BTC]
        :return:
        """
        print('Subscribe Ticker')
        def subscribe_ticker():
            # key=time rounded to minute, value is dict with volume, price, type (buy, sell)
            ticker_data = {}

            def store_data_in_db():
                for timestamp, data in ticker_data.items():
                    if (timestamp + 60) < datetime.now().timestamp():

                        print('Storing Data')
                        temp_data = ticker_data.pop(timestamp, None)

                        with self._db_helper.db_session() as session:
                            for product, product_v in temp_data.items():
                                for curr, curr_v in product_v.items():

                                    # price = sum(temp_data.get('price')) / len(temp_data.get('price'))

                                    # Get close price aka last price added to list
                                    price = curr_v.get('price')[-1]

                                    buy = [curr_v.get('size')[i] for i, side in enumerate(curr_v.get('side')) if side == 'buy']
                                    sell = [curr_v.get('size')[i] for i, side in enumerate(curr_v.get('side')) if side == 'sell']

                                    buy_volume =  sum(buy)
                                    sell_volume = sum(sell)
                                    try:
                                        coin = self._db_helper.build_coin(
                                            value=price,
                                            buy_volume=buy_volume,
                                            sell_volume=sell_volume,
                                            coin_symbol=product,
                                            market_symbol=curr,
                                            timestamp=timestamp
                                        )
                                        session.add(coin)
                                        print(f'Added Coin to DB')
                                    except Exception as e:
                                        print(e)
                            session.commit()

            def process_data(ws, message: str):
                message_json = json.loads(message)
                if message_json.get('type') != 'ticker':
                    return

                # TODO remove
                if type(message_json) != dict:
                    print(f'Message is not dict: {message_json}')

                ticker = message_json

                ticker_date = datetime.strptime(ticker['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                min_timestamp = int(ticker_date.replace(tzinfo = timezone.utc).timestamp() - ticker_date.second)
                min_data = ticker_data.get(min_timestamp)

                product, curr = ticker.get('product_id').split('-')

                if not min_data:
                    ticker_data[min_timestamp] = {
                        product: {
                            curr: {
                                'price': [float(ticker['price'])],
                                'side': [ticker['side']],
                                'size': [float(ticker['last_size'])]
                            }
                        }
                    }
                else:
                    min_data[product][curr]['price'].append(float(ticker['price']))
                    min_data[product][curr]['side'].append(ticker['side'])
                    min_data[product][curr]['size'].append(float(ticker['last_size']))

                store_data_in_db()

            ws = GDAXWebsocket()
            ws.ticker_channel_socket(process_data_func=process_data, product_ids=product_ids)


        Thread(target=subscribe_ticker).start()



