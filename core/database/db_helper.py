import time
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from core.database.model import Coin, EMA

HOUR = 3600
NUM_LABELS = 12

DB_URL =  'sqlite:///app.db'

class DBHelper:

    def __init__(self, engine):
        self.__engine = engine
        self.__session = sessionmaker(bind=self.__engine)

    @contextmanager
    def db_session(self):
        session = self.__session()
        yield session
        session.close()

    @staticmethod
    def retrieve_graph_data_for_time_period(coin_data):
        """
        :param coin_data:
        :return:
        """
        graph_data = {'data': []}

        if coin_data:
            min_value = max_value = coin_data[0].value_market
            for coin in coin_data:
                if coin.value_market > max_value:
                    max_value = coin.value_market
                elif coin.value_market < min_value:
                    min_value = coin.value_market
                graph_data['data'].append([coin.date * 1000, coin.value_market])

            graph_data['min'] = min_value
            graph_data['max'] = max_value
            graph_data['num_labels'] = NUM_LABELS
        return graph_data

    @staticmethod
    def get_delete_time(time_period_hours=168):
        time_period_milli = time_period_hours * HOUR
        time_now = time.time()
        delete_time = time_now - time_period_milli
        return delete_time

    def delete_old_coin(self, time_period_hours: int = 6):
        """
        Delete old data from database
        :return:
        """
        delete_time = self.get_delete_time(time_period_hours=time_period_hours)
        with self.db_session() as session:
            coin_data = session.query(Coin).all()
            for coin in coin_data:
                if coin.date < delete_time:
                    session.delete(coin)

            ema_data = session.query(EMA).all()
            for ema in ema_data:
                if ema.date < delete_time:
                    session.delete(ema)

            session.commit()

    def build_coin(self, value, buy_volume, sell_volume, coin_symbol, market_symbol, timestamp) -> Coin:
        """
        Save coin value to database
        :param value:
        :param buy_volume
        :param sell_volume
        :param coin_symbol:
        :param market_symbol:
        :param timestamp
        :return:
        """
        return Coin(
            coin_symbol=coin_symbol,
            market_coin_symbol=market_symbol,
            value_market=value,
            buy_volume=buy_volume,
            sell_volume=sell_volume,
            date=timestamp
        )

    def build_ema(self, ema_values: [], symbol, market_coin_symbol, timestamp) -> EMA:
        return EMA(
            coin_symbol=symbol,
            market_coin_symbol=market_coin_symbol,
            value_five=ema_values[0],
            value_twelve=ema_values[1],
            value_twenty_six=ema_values[2],
            value_fifty=ema_values[3],
            date=timestamp
        )

    def commit_coin_value(self, value, volume, symbol, market_coin_symbol, timestamp):
        """
        Save coin value to database
        :param value:
        :param volume
        :param symbol:
        :param market_coin_symbol:
        :param timestamp
        :param commit
        :return:
        """
        coin = Coin(
            coin_symbol=symbol,
            market_coin_symbol=market_coin_symbol,
            value_market=value,
            buy_volume=volume,
            date=timestamp
        )

        with self.db_session() as session:
            session.add(coin)
            session.commit()

    def commit_ema(self, ema_values: [], symbol, market_coin_symbol, timestamp):
        """

        :param ema_values:
        :param symbol:
        :param market_coin_symbol:
        :param timestamp:
        :param commit:
        :return:
        """
        ema = EMA(
            coin_symbol=symbol,
            market_coin_symbol=market_coin_symbol,
            value_five=ema_values[0],
            value_twelve=ema_values[1],
            value_twenty_six=ema_values[2],
            value_fifty=ema_values[3],
            date=timestamp
        )

        with self.db_session() as session:
            session.add(ema)
            session.commit()

    def query_coin_db(self, symbol, market_coin_symbol):
        """
        Query database for all coin data
        :param symbol:
        :param market_coin_symbol:
        :return:
        """
        self.delete_old_coin()

        with self.db_session() as session:

            coin_data = session.query(Coin).filter_by(coin_symbol=symbol, market_coin_symbol=market_coin_symbol
                                                      ).order_by(Coin.id.desc()).limit(300).all()
            coin_data = list(reversed(coin_data))
            query_graph_data = {
                'price': self.retrieve_graph_data_for_time_period(coin_data=coin_data),
                'label': "{}/{}".format(symbol, market_coin_symbol),
                'ema5': [],
                'ema12': [],
                'ema26': [],
                'ema50': []
            }
            ema_data = session.query(EMA).filter_by(coin_symbol=symbol, market_coin_symbol=market_coin_symbol
                                           ).order_by(EMA.id.desc()).limit(300).all()
        ema_data = list(reversed(ema_data))

        for ema in ema_data:
            query_graph_data['ema5'].append([ema.date * 1000, ema.value_five])
            query_graph_data['ema12'].append([ema.date * 1000, ema.value_twelve])
            query_graph_data['ema26'].append([ema.date * 1000, ema.value_twenty_six])
            query_graph_data['ema50'].append([ema.date * 1000, ema.value_fifty])

        return query_graph_data
