from flask import Flask, jsonify, request, session
from core.database.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template
import datetime
from core.binance.binance_trader import BinanceTrader



app = Flask(__name__)
app.config.from_object(Config)
coin_db = SQLAlchemy(app)
migrate = Migrate(app, coin_db)
binance_trader = None
api_key = 'Xwme4vyRvhCSRZzJDpqgzTllB2WyrfKG5hpeHEXRjQ4XEg9iOK41tJxiQlIgsRfI'
api_secret = 'JofglM7AOlroYhca0sFIHX6KsTqTuIs6S27w7EBr97DpWTV6VWReOO0AfzW180I5'
binance_trader = BinanceTrader(api_key=api_key, api_secret=api_secret)


# DB setup
class Coin(coin_db.Model):
    id = coin_db.Column(coin_db.Integer, primary_key=True)
    coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    market_coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    value_market = coin_db.Column(coin_db.String(64), index=True, unique=False)
    date = coin_db.Column(coin_db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Coin {}>'.format(self.symbol)


coin_db.create_all()


# API
@app.route('/time')
def get_time():
    time = datetime.datetime.now()
    return jsonify(time)


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


@app.route('/update')
def update():
    global binance_trader, coin_db
    data = {}
    if binance_trader is not None:
        symbol = 'BNB'
        value = binance_trader.get_last_bid(symbol)
        session[symbol] = value
        coin = Coin(
            coin_symbol=symbol,
            market_coin_symbol='ETH',
            value_market=value,
            date=str(datetime.datetime.now())
        )
        coin_db.session.add(coin)
        coin_db.session.commit()
        data = {'value': value}
    return jsonify(data)


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
    time = datetime.datetime.now()
    return render_template('index.html', title='CoinCollector', user=user, time=time)

app.run()
