from sqlalchemy import Column, Integer, Float, String

from frontend import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True)
    coin_symbol = Column(String(64), index=True, unique=False)
    market_coin_symbol = Column(String(64), index=True, unique=False)
    value_market = Column(Float, index=True, unique=False)
    buy_volume = Column(Float, index=True, unique=False)
    sell_volume = Column(Float, index=True, unique=False)
    date = Column(Float, index=True, unique=False)

    def __repr__(self):
        return '<Coin {}>'.format(self.symbol)


class EMA(Base):
    __tablename__ = "emas"

    id = Column(Integer, primary_key=True)
    coin_symbol = Column(String(64), index=True, unique=False)
    market_coin_symbol = Column(String(64), index=True, unique=False)
    value_five = Column(Float, index=True, unique=False)
    value_twelve = Column(Float, index=True, unique=False)
    value_twenty_six = Column(Float, index=True, unique=False)
    value_fifty = Column(Float, index=True, unique=False)
    date = Column(Float, index=True, unique=False)

    def __repr__(self):
        return '<EMA12 {}>'.format(self.symbol)