from flask_sqlalchemy import SQLAlchemy

coin_db = SQLAlchemy()


class Coin(coin_db.Model):
    id = coin_db.Column(coin_db.Integer, primary_key=True)
    coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    market_coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    value_market = coin_db.Column(coin_db.Float, index=True, unique=False)
    date = coin_db.Column(coin_db.Float, index=True, unique=False)

    def __repr__(self):
        return '<Coin {}>'.format(self.symbol)


class EMA(coin_db.Model):
    id = coin_db.Column(coin_db.Integer, primary_key=True)
    coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    market_coin_symbol = coin_db.Column(coin_db.String(64), index=True, unique=False)
    value_five = coin_db.Column(coin_db.Float, index=True, unique=False)
    value_twelve = coin_db.Column(coin_db.Float, index=True, unique=False)
    value_twenty_six = coin_db.Column(coin_db.Float, index=True, unique=False)
    value_fifty = coin_db.Column(coin_db.Float, index=True, unique=False)
    date = coin_db.Column(coin_db.Float, index=True, unique=False)

    def __repr__(self):
        return '<EMA12 {}>'.format(self.symbol)