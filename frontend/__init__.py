from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.database.config import Config

app = Flask(__name__)
app.config.from_object(Config)
coin_db = SQLAlchemy()

from core.collector import Collector
from core.database.db_helper import DBHelper
from core.enums import Currencies

coin_db.init_app(app)
db_help = DBHelper(coin_db)
collector = Collector(db_help)


def create_app():
    with app.app_context():

        from frontend.blueprints import coin_collector
        app.register_blueprint(coin_collector.coin_collector_blueprint)

        collector.add_trading_pair(Currencies.ETH, Currencies.USD)
        # collector.add_trading_pair(Currencies.ETH, Currencies.BTC)

    coin_db.init_app(app)
    coin_db.create_all(app=app)
    return app
