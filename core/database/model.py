import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime

from frontend import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True)
    coin_symbol = Column(String(64), index=True, unique=False)
    market_coin_symbol = Column(String(64), index=True, unique=False)
    value_market = Column(Float, unique=False)
    buy_volume = Column(Float, unique=False)
    sell_volume = Column(Float, unique=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Coin {}>'.format(self.symbol)


class EMA(Base):
    __tablename__ = "emas"

    id = Column(Integer, primary_key=True)
    coin_symbol = Column(String(64), index=True, unique=False)
    market_coin_symbol = Column(String(64), index=True, unique=False)
    value_five = Column(Float, unique=False)
    value_twelve = Column(Float,  unique=False)
    value_twenty_six = Column(Float, unique=False)
    value_fifty = Column(Float, unique=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<EMA12 {}>'.format(self.symbol)

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    coin_symbol = Column(String(64), index=True, unique=False)
    market_coin_symbol = Column(String(64), index=True, unique=False)
    value_market = Column(Float, unique=False)
    amount = Column(Float, unique=False)
    buy_sell = Column(String(64), unique=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Trade {}>'.format(self.symbol)
