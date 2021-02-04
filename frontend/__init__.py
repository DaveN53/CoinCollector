from flask import Flask

from core.database.config import Config
from core.database.db_helper import DBHelper
from core.database.db_manager import coin_db
from core.trade.coin_trader import CoinTrader

app = Flask(__name__)
app.config.from_object(Config)
exchange_trader = CoinTrader()
db_help = DBHelper()


def create_app():
    with app.app_context():

        from frontend.blueprints import coin_collector, exchange_api
        app.register_blueprint(coin_collector.coin_collector_blueprint)
        app.register_blueprint(exchange_api.exchange_blueprint)

    coin_db.init_app(app)
    coin_db.create_all(app=app)
    return app
