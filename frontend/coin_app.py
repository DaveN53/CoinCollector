from flask import Flask, jsonify, request, session, redirect
from core.database.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
import time
from core.binance.binance_trader import BinanceTrader
from core.coin_trader import CoinTrader
from core.database.db_helper import DBHelper



app = Flask(__name__)
app.config.from_object(Config)
coin_db = SQLAlchemy(app)
migrate = Migrate(app, coin_db)
exchange_trader = CoinTrader()
db_help = DBHelper()


# DB setup
class Coin(coin_db.Model):
    id = coin_db.Column(coin_db.Integer, primary_key=True)
    coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    market_coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    value_market = coin_db.Column(coin_db.Float, index=True, unique=False)
    date = coin_db.Column(coin_db.Float, index=True, unique=False)

    def __repr__(self):
        return '<Coin {}>'.format(self.symbol)


coin_db.create_all()


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
    graph_data = query_coin_db(symbol, market_coin_symbol)

    value = 0
    if graph_data['data']:
        value = graph_data['data'][len(graph_data['data'])-1][1]
    data = {
        'value': value,
        'graph_data': graph_data
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
        result = exchange_trader.make_decision()

    return jsonify(data)


def update_coin_data(coin_symbol, market_symbol):
    """
    :param coin_symbol: Coin you're interested
    :param market_symbol: symbol to represent value. USD, GDP, BTC
    :return:
    """
    global exchange_trader, db_help
    value = exchange_trader.price
    commit_coin_value(value, coin_symbol, market_symbol)
    graph_data = query_coin_db(coin_symbol, market_symbol)
    data = {
        'value': value,
        'graph_data': graph_data
    }
    return data


def commit_coin_value(value, symbol, market_coin_symbol):
    """
    Save coin value to database
    :param value:
    :param symbol:
    :param market_coin_symbol:
    :return:
    """
    coin = Coin(
        coin_symbol=symbol,
        market_coin_symbol=market_coin_symbol,
        value_market=value,
        date=str(time.time())
    )
    coin_db.session.add(coin)
    coin_db.session.commit()


def query_coin_db(symbol, market_coin_symbol):
    """
    Query database for all coin data
    :param symbol:
    :param market_coin_symbol:
    :return:
    """
    delete_old_coin()
    coin_data = Coin.query.filter_by(coin_symbol=symbol).all()
    graph_data = db_help.retrieve_graph_data_for_time_period(coin_data=coin_data)
    graph_data['label'] = "{}/{}".format(symbol, market_coin_symbol)
    return graph_data


def delete_old_coin():
    """
    Delete old data from database
    :return:
    """
    delete_time = db_help.get_delete_time(time_period_hours=6)
    coin_data = Coin.query.all()
    for coin in coin_data:
        if coin.date < delete_time:
            coin_db.session.delete(coin)
    coin_db.session.commit()


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

app.run()
