from core.enums import OrderAction


class Exchange:

    def __init__(self):
        self._last_sold = 0
        self._last_buy = 0

    @property
    def current_price(self):
        raise NotImplementedError

    @property
    def last_sold_price(self):
        return self._last_sold

    @property
    def last_buy_price(self):
        return self._last_buy

    def get_candles(self):
        raise NotImplementedError

    def create_stop_limit_order(self, current_price: float, action: OrderAction):
        pass
