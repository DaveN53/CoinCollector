from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from core.database.config import Config

app = Flask(__name__)
app.config.from_object(Config)

DB_URL =  'sqlite:///app.db'
engine = create_engine(
    DB_URL
)
Base = declarative_base()

from core.collector import Collector
from core.database.db_helper import DBHelper
from core.enums import Currencies

db_help = DBHelper(engine)
collector = Collector(db_help)


def create_app():
    with app.app_context():

        from frontend.blueprints import coin_collector
        app.register_blueprint(coin_collector.coin_collector_blueprint)

        collector.add_trading_pair(Currencies.ETH, Currencies.USD)
        # collector.add_trading_pair(Currencies.ETH, Currencies.BTC)

        collector.subscribe_ticker_socket()

    Base.metadata.create_all(engine)
    return app
