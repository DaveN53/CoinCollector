from flask import Blueprint, session, jsonify, request
from werkzeug.utils import redirect

from frontend import exchange_trader

exchange_blueprint = Blueprint('exchange_blueprint', __name__, template_folder='..\\templates')


@exchange_blueprint.route('/buy/rate/<symbol>')
def get_buy_rate(symbol=None):
    data = {}
    if symbol is not None and exchange_trader is not None:
        session['buy'] = exchange_trader.get_last_bid(symbol)
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