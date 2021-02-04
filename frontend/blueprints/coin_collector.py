import time
from flask import Blueprint, render_template, jsonify

from core.database.db_manager import coin_db
from core.trend_helper import TrendHelper
from frontend import exchange_trader, db_help

coin_collector_blueprint = Blueprint('coin_collector_blueprint', __name__, template_folder='..\\templates')


@coin_collector_blueprint.route('/')
def index():
    user = {'username': 'David'}
    return render_template('index.html', title='CoinCollector', user=user, time=time.time())


@coin_collector_blueprint.route('/graph')
def create_graph():
    """
    Runs once when page is loaded to create graph
    :return:
    """
    symbol = 'ETH'
    market_coin_symbol = 'USD'
    db_help.delete_old_coin()
    graph_data = db_help.query_coin_db(symbol, market_coin_symbol)
    if not graph_data['price']['data']:
        candles = exchange_trader.candles
        price_data = []
        for idx, candle in enumerate(reversed(candles)):
            price_data.append(candle[4])
            try:
                ema_data = TrendHelper.ema_snapshot(price_data[:idx])
                db_help.commit_ema(
                    [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
                    symbol,
                    market_coin_symbol,
                    candle[0],
                    commit=False)
            except ValueError:
                pass
            db_help.commit_coin_value(candle[4], symbol, market_coin_symbol, candle[0], commit=False)
        coin_db.session.commit()
    graph_data = db_help.query_coin_db(symbol, market_coin_symbol)
    value = exchange_trader.current_price
    data = {
        'value': value,
        'graph_data': graph_data['price'],
        'ema5': graph_data['ema5'],
        'ema12': graph_data['ema12'],
        'ema26': graph_data['ema26'],
        'ema50': graph_data['ema50'],
        'label': graph_data['label']
    }
    return jsonify(data)


@coin_collector_blueprint.route('/update')
def update():
    """
    Runs every minute to update price data
    :return:
    """
    data = {}
    if exchange_trader is not None:
        data = update_coin_data('ETH', 'USD')
        # result = exchange_trader.make_decision(data)

    return jsonify(data)


def update_coin_data(coin_symbol, market_symbol):
    """
    :param coin_symbol: Coin you're interested
    :param market_symbol: symbol to represent value. USD, GDP, BTC
    :return:
    """
    timestamp = str(time.time())
    value = exchange_trader.current_price
    db_help.commit_coin_value(value, coin_symbol, market_symbol, timestamp)
    graph_data = db_help.query_coin_db(coin_symbol, market_symbol)
    try:
        price_data = []
        for data in graph_data['price']['data']:
            price_data.append(data[1])
        ema_data = TrendHelper.ema_snapshot(price_data)
        db_help.commit_ema(
            [ema_data['EMA5'], ema_data['EMA12'], ema_data['EMA26'], ema_data['EMA50']],
            coin_symbol,
            market_symbol,
            timestamp)

    except ValueError:
        pass
    graph_data = db_help.query_coin_db(coin_symbol, market_symbol)
    data = {
        'time': 'current_time',
        'value': value,
        'graph_data': graph_data['price'],
        'ema5': graph_data['ema5'],
        'ema12': graph_data['ema12'],
        'ema26': graph_data['ema26'],
        'ema50': graph_data['ema50'],
        'label': graph_data['label'],
    }
    return data