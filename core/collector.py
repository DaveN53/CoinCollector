import concurrent.futures
from typing import List, Dict

import time

from core.database.db_helper import DBHelper
from core.enums import ExchangeName
from core.exchange.GDAX.gdax_trader import GDAXTrader
from core.exchange.exchange import Exchange
from core.trade.indicator.ema_crossover import EMACrossover
from core.trade.indicator.indicator import Indicator
from core.trend_helper import TrendHelper
from core.utilities import get_seperate_data_list


class Collector:

    def __init__(self, db_helper: DBHelper, exchange_name: ExchangeName = ExchangeName.GDAX):
        """
        active_coin_pairs: Coin paris to actively track and trade on
        positions: current holdings for all crypto + USD
        """

        self._db_helper = db_helper
        self._exchange = self._setup_exchange(exchange_name)
        self._indicators = self._setup_indicators()
        self._active_coin_pairs: Dict = {}
        self._positions: List[dict] = []

    def _setup_exchange(self, exchange_name: ExchangeName = ExchangeName.GDAX) -> Exchange:
        """
        Build the exchange object we'll be using
        :param exchange_name:
        :return:
        """
        if exchange_name is ExchangeName.GDAX:
            return GDAXTrader(self._db_helper)
        # elif exchange_name is ExchangeName.BINANCE:
        #     return BinanceTrader(
        #         api_key=os.environ.get('BINANCE_KEY'),
        #         api_secret=os.environ.get('BINANCE_SECRET'))

    def _setup_indicators(self) -> List[Indicator]:
        indicators = [
            EMACrossover()
        ]
        return indicators

    def add_trading_pair(self, coin_symbol: str, market_symbol: str):
        """
        Add coin / market pair
        :param coin_symbol:
        :param market_symbol:
        :return:
        """
        existing_coin = self._active_coin_pairs.get(coin_symbol)
        if not existing_coin:
            self._active_coin_pairs[coin_symbol] = [market_symbol]
        else:
            if market_symbol in existing_coin:
                return
            existing_coin.append(market_symbol)

    def subscribe_ticker_socket(self):
        product_ids = []
        for k, v in self._active_coin_pairs.items():
            product_ids.extend([f'{k}-{curr}' for curr in v])

        self._exchange.subscribe_ticker_channel(product_ids=product_ids)

    def get_candle_graph_data(self):
        # TODO handle multiple coins at once
        symbol = 'ETH'
        market_coin_symbol = 'USD'
        self._db_helper.delete_old_coin()
        graph_data = self._db_helper.query_coin_db(symbol, market_coin_symbol)
        if not graph_data['price']['data']:
            candles = self._exchange.get_candles(symbol, market_coin_symbol)
            # candles = exchange_trader.candles
            price_data = []
            with self._db_helper.db_session() as session:
                for idx, candle in enumerate(reversed(candles)):
                    price_data.append(candle[4])
                    try:
                        ema_data = TrendHelper.ema_snapshot(price_data[:idx])
                        ema = self._db_helper.build_ema(
                            [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
                            symbol,
                            market_coin_symbol,
                            candle[0])
                        session.add(ema)
                    except ValueError:
                        pass
                    price_time = candle[0]
                    close_price, volume = candle[4:6]
                    coin = self._db_helper.build_coin(close_price, volume, None, symbol, market_coin_symbol, price_time)
                    session.add(coin)
                session.commit()
        graph_data = self._db_helper.query_coin_db(symbol, market_coin_symbol)

        macd_data = self.calculate_macd(graph_data)

        len_diff = len(graph_data['price']['data']) - len(graph_data['ema12'])
        graph_data['price']['data'] = graph_data['price']['data'][len_diff:]

        data = {
            'value': graph_data['price']['data'][-1][1],
            'graph_data': graph_data['price'],
            'ema5': graph_data['ema5'],
            'ema12': graph_data['ema12'],
            'ema26': graph_data['ema26'],
            'ema50': graph_data['ema50'],
            'macd': macd_data[0],
            'ema9': macd_data[1],
            'label': graph_data['label']
        }
        return data

    def get_graph_data(self):
        # TODO handle multiple coins at once
        coin_symbol = 'ETH'
        market_symbol = 'USD'

        self.calculate_ema()

        graph_data = self._db_helper.query_coin_db(coin_symbol, market_symbol)

        macd_data = self.calculate_macd(graph_data)

        len_diff = len(graph_data['price']['data']) - len(graph_data['ema12'])
        graph_data['price']['data'] = graph_data['price']['data'][len_diff:]

        data = {
            'time': 'current_time',
            'value': graph_data['price']['data'][-1][1],
            'graph_data': graph_data['price'],
            'ema5': graph_data['ema5'],
            'ema12': graph_data['ema12'],
            'ema26': graph_data['ema26'],
            'ema50': graph_data['ema50'],
            'macd': macd_data[0],
            'ema9': macd_data[1],
            'label': graph_data['label'],
        }
        return data

    def calculate_ema(self):
        # TODO handle multiple coins at once
        timestamp = str(time.time())
        coin_symbol = 'ETH'
        market_symbol = 'USD'

        graph_data = self._db_helper.query_coin_db(coin_symbol, market_symbol)
        try:
            price_data = []
            for data in graph_data['price']['data']:
                price_data.append(data[1])
            ema_data = TrendHelper.ema_snapshot(price_data)
            self._db_helper.commit_ema(
                [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
                coin_symbol,
                market_symbol,
                timestamp)
        except ValueError:
            pass

    def calculate_macd(self, graph_data: dict):
        ema_12, time_data = get_seperate_data_list(graph_data.get('ema12'))
        ema_26, _ = get_seperate_data_list(graph_data.get('ema26'))
        md, em9 = TrendHelper.calculate_moving_average_convergence_divergence(ema_12, ema_26)

        macd = []
        ema_9 = []
        len_diff = len(md) - len(em9)

        md = md[len_diff:]
        time_data = time_data[len_diff:]

        for idx, price_time in enumerate(time_data):
            macd.append([price_time, md[idx]])
            ema_9.append([price_time, em9[idx]])

        return macd, ema_9

    def analyze(self, data: dict):
        """
        Run Algos to analyze data and make a trade decision
        Algo results will be a float in the range 0.0 to 10.0
        0.0 is bearish, 10.0 is bullish
        :return:
        """
        # TODO Volume indicator is next

        results = [indicator.get_result(data) for indicator in self._indicators]
        average = sum(results) / len(results)

        # print(f'{datetime.datetime.now()}: Indicator Average {average}')

        # Based on average make a buy/sell decision