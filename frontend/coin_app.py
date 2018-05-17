from flask import Flask, jsonify, request, session, redirect
from core.database.config import Config
from flask_migrate import Migrate
from flask import render_template
import time
from core.trend_helper import TrendHelper
from core.coin_trader import CoinTrader
from core.database.db_helper import DBHelper
from core.database.db_manager import coin_db


app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, coin_db)
exchange_trader = CoinTrader()
db_help = DBHelper()

# API
@app.route('/time')
def get_time():
    return jsonify(time.time())


@app.route('/buy/rate/<symbol>')
def get_buy_rate(symbol=None):
    global binance_trader
    data = {}
    if symbol is not None and binance_trader is not None:
        session['buy'] = binance_trader.get_last_bid(symbol)
        data = {
            'symbol': symbol,
            'value': session['buy']
        }
    return jsonify(data)


@app.route('/bid', methods=['POST', 'GET'])
def bid():
    bid_price = request.form['bid_price']
    print(bid_price)
    return redirect('/')


@app.route('/graph')
def graph_data():
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
    value = exchange_trader.price
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


@app.route('/update')
def update():
    """
    Runs every minute to update price data
    :return:
    """
    global coin_db
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
    global exchange_trader, db_help
    timestamp = str(time.time())
    value = exchange_trader.price
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
        'value': value,
        'graph_data': graph_data['price'],
        'ema5': graph_data['ema5'],
        'ema12': graph_data['ema12'],
        'ema26': graph_data['ema26'],
        'ema50': graph_data['ema50'],
        'label': graph_data['label'],
    }
    return data


@app.route('/database')
def show_entries():
    global coin_db
    db = coin_db
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return jsonify(entries)

#URL
@app.route('/')
@app.route('/index')
def index(data=''):
    user = {'username': 'David'}
    return render_template('index.html', title='CoinCollector', user=user, time=time.time())

coin_db.init_app(app)
coin_db.create_all(app=app)
app.run()
