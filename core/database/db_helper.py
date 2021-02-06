import time

from flask_sqlalchemy import SQLAlchemy

from core.database.model import Coin, EMA

HOUR = 3600
NUM_LABELS = 12


class DBHelper:

    def __init__(self, db: SQLAlchemy):
        self._coin_db = db

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

    def delete_old_coin(self):
        """
        Delete old data from database
        :return:
        """
        delete_time = self.get_delete_time(time_period_hours=66)
        coin_data = Coin.query.all()
        for coin in coin_data:
            if coin.date < delete_time:
                self._coin_db.session.delete(coin)

        ema_data = EMA.query.all()
        for ema in ema_data:
            if ema.date < delete_time:
                self._coin_db.session.delete(ema)

        self._coin_db.session.commit()

    def commit(self):
        self._coin_db.session.commit()

    def add_coin_value(self, value, coin_symbol, market_symbol, timestamp):
        """
        Save coin value to database
        :param value:
        :param coin_symbol:
        :param market_symbol:
        :param timestamp
        :param commit
        :return:
        """
        coin = Coin(
            coin_symbol=coin_symbol,
            market_coin_symbol=market_symbol,
            value_market=value,
            date=timestamp
        )
        self._coin_db.session.add(coin)

    def commit_coin_value(self, value, symbol, market_coin_symbol, timestamp, commit: bool = True):
        """
        Save coin value to database
        :param value:
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
            date=timestamp
        )
        self._coin_db.session.add(coin)
        if commit:
            self._coin_db.session.commit()

    def commit_ema(self, ema_values: [], symbol, market_coin_symbol, timestamp, commit: bool = True):
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
        self._coin_db.session.add(ema)
        if commit:
            self._coin_db.session.commit()

    def query_coin_db(self, symbol, market_coin_symbol):
        """
        Query database for all coin data
        :param symbol:
        :param market_coin_symbol:
        :return:
        """
        self.delete_old_coin()
        coin_data = Coin.query.filter_by(coin_symbol=symbol, market_coin_symbol=market_coin_symbol
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
        ema_data = EMA.query.filter_by(coin_symbol=symbol, market_coin_symbol=market_coin_symbol
                                       ).order_by(EMA.id.desc()).limit(300).all()
        ema_data = list(reversed(ema_data))

        for ema in ema_data:
            query_graph_data['ema5'].append([ema.date * 1000, ema.value_five])
            query_graph_data['ema12'].append([ema.date * 1000, ema.value_twelve])
            query_graph_data['ema26'].append([ema.date * 1000, ema.value_twenty_six])
            query_graph_data['ema50'].append([ema.date * 1000, ema.value_fifty])

        return query_graph_data
