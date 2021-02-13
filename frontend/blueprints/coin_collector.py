import time
from threading import Thread

from flask import Blueprint, render_template, jsonify

from frontend import collector

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
    collector.get_candle_graph_data()
    data = collector.get_graph_data()
    return jsonify(data)


@coin_collector_blueprint.route('/update')
def update():
    """
    Runs every minute to update price data
    :return:
    """
    # collector.get_latest_coin_data()  # This is done in a thread w/ the WS
    data = collector.get_graph_data()

    # Analyze on a thread so we don't hold up the UI
    Thread(target=collector.analyze, args=(data,)).start()

    return jsonify(data)
