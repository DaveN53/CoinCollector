from datetime import datetime, timedelta
from typing import List, Dict

from core.database.db_helper import DBHelper
from core.enums import ExchangeName, TradeAction
from core.exchange.GDAX.gdax_trader import GDAXTrader
from core.exchange.exchange import Exchange
from core.trade.indicator.indicator import Indicator
from core.trend_helper import TrendHelper
from core.utilities import get_seperate_data_list, get_hc_timestamp, get_dt_hc
from trade.indicator.moving_average_convergence_divergence import MACD


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
            MACD()
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
        if not graph_data['price']:
            candles = self._exchange.get_candles(symbol, market_coin_symbol)
            # candles = exchange_trader.candles
            price_data = []
            with self._db_helper.db_session() as session:
                for idx, candle in enumerate(reversed(candles)):
                    price_data.append(candle[4])
                    price_time_utc = datetime.fromtimestamp(candle[0]) + timedelta(hours=5)
                    try:
                        ema_data = TrendHelper.ema_snapshot(price_data[:idx])
                        ema = self._db_helper.build_ema(
                            [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
                            symbol,
                            market_coin_symbol,
                            price_time_utc)
                        session.add(ema)
                    except ValueError:
                        pass
                    close_price, volume = candle[4:6]
                    coin = self._db_helper.build_coin(close_price, volume, None, symbol, market_coin_symbol, price_time_utc)
                    session.add(coin)
                session.commit()

    def get_graph_data(self):
        # TODO handle multiple coins at once
        coin_symbol = 'ETH'
        market_symbol = 'USD'

        graph_data = self._db_helper.query_coin_db(coin_symbol, market_symbol)

        graph_data = self.calculate_ema(graph_data)
        graph_data = self.calculate_macd(graph_data)

        trade_data = self.get_trade_data()

        len_diff = len(graph_data['price']) - len(graph_data['ema12'])
        graph_data['price'] = graph_data['price'][len_diff:]

        data = {
            'time': 'current_time',
            'value': graph_data['price'][-1][1],
            'price': graph_data['price'],
            'volume': graph_data['volume'],
            'ema5': graph_data['ema5'],
            'ema12': graph_data['ema12'],
            'ema26': graph_data['ema26'],
            'ema50': graph_data['ema50'],
            'macd': graph_data['macd'],
            'ema9': graph_data['ema9'],
            'label': graph_data['label'],
            'buy': trade_data.get('buy'),
            'sell': trade_data.get('sell')
        }
        return data

    def get_trade_data(self):
        coin_symbol = 'ETH'
        market_symbol = 'USD'

        trade_data = self._db_helper.query_trades(coin_symbol, market_symbol)

        return {
            'buy': [[get_hc_timestamp(trade.date), trade.value_market] for trade in trade_data if trade.buy_sell == TradeAction.BUY.value],
            'sell': [[get_hc_timestamp(trade.date), trade.value_market] for trade in trade_data if trade.buy_sell == TradeAction.SELL.value]
        }


    def calculate_ema(self, graph_data: dict):
        # TODO handle multiple coins at once
        coin_symbol = 'ETH'
        market_symbol = 'USD'

        try:
            timestamp = get_dt_hc(graph_data['price'][-1][0])
            price_data = []
            for data in graph_data['price']:
                price_data.append(data[1])
            ema_data = TrendHelper.ema_snapshot(price_data)
            self._db_helper.commit_ema(
                [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
                coin_symbol,
                market_symbol,
                timestamp)
        except ValueError:
            pass

        ema_data = self._db_helper.query_ema(coin_symbol, market_symbol)
        for ema in ema_data:
            graph_data['ema5'].append([get_hc_timestamp(ema.date), ema.value_five])
            graph_data['ema12'].append([get_hc_timestamp(ema.date), ema.value_twelve])
            graph_data['ema26'].append([get_hc_timestamp(ema.date), ema.value_twenty_six])
            graph_data['ema50'].append([get_hc_timestamp(ema.date), ema.value_fifty])

        return graph_data

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

        graph_data['macd'] = macd
        graph_data['ema9'] = ema_9

        return graph_data

    def analyze(self, data: dict):
        """
        Run Algos to analyze data and make a trade decision
        Algo results will be a float in the range -10.0 to 10.0
        -10.0 is bearish, 10.0 is bullish
        :return:
        """

        # Indicator 2/3 majority
        sig_majority = 6.66

        # TODO Volume indicator is next
        signals = []
        results = [indicator.get_result(data) for indicator in self._indicators]
        for result in results:
            signals.extend(result)

        print(f'Signals: {signals}')
        if signals:
            average = sum(signals) / len(signals)
            print(f'Signal average: {average}')

            if average >= sig_majority:
                print('BUYING')
                self.buy_coin(data)

            if average <= -sig_majority:
                print('SELLING')
                self.sell_coin(data)

    def buy_coin(self, data):
        timestamp, price = data['graph_data']['data'][-1]
        dt = get_dt_hc(timestamp)

        # TODO don't hardcode symbol
        with self._db_helper.db_session() as session:
            trade = self._db_helper.build_trade('ETH', 'USD', price, .75, TradeAction.BUY.value, dt)
            session.add(trade)
            session.commit()

    def sell_coin(self, data):
        timestamp, price = data['graph_data']['data'][-1]
        dt = get_dt_hc(timestamp)

        # TODO don't hardcode symbol
        with self._db_helper.db_session() as session:
            trade = self._db_helper.build_trade('ETH', 'USD', price, .75, TradeAction.SELL.value, dt)
            session.add(trade)
            session.commit()
