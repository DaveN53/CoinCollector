from flask import Blueprint, session, jsonify, request
from werkzeug.utils import redirect

exchange_blueprint = Blueprint('exchange_blueprint', __name__, template_folder='..\\templates')


@exchange_blueprint.route('/buy/rate/<symbol>')
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


@exchange_blueprint.route('/bid', methods=['POST', 'GET'])
def bid():
    bid_price = request.form['bid_price']
    print(bid_price)
    return redirect('/')