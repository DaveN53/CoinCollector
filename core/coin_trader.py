from core.binance.binance_trader import BinanceTrader
from core.GDAX.gdax_trader import GDAXTrader
from core.enums import OrderBook, OrderAction


class Exchange:
    GDAX = 'GDAX'
    BINANCE = 'BINANCE'


class CoinTrader:

    def __init__(self, buying: bool = True, exchange: Exchange = Exchange.GDAX ):
        self.gdax_trader = GDAXTrader()
        self.exchange = exchange
        self.exchange_trader = None
        self.selling = not buying
        self.buying = buying
        self.setup_exchange()
        self.current_price = self.exchange_trader.price

    def setup_exchange(self):
        if self.exchange is Exchange.GDAX:
            self.exchange_trader = GDAXTrader()
        elif self.exchange is Exchange.BINANCE:
            self.binance_api_key = ''
            self.binance_api_secret = ''
            self.exchange_trader = BinanceTrader()

    @property
    def price(self):
        self.current_price =  self.exchange_trader.price
        return self.current_price

    @property
    def candles(self):
        return self.exchange_trader.get_candles()

    def make_decision(self):
        """
        :return: result of decision
        """
        result = None
        if self.selling:
            result = self.make_sell_decision()
        elif self.buying:
            result = self.make_buy_decision()

        return result

    def make_buy_decision(self):
        """
        Check current price
        Check last buy limit / last sell
        If current < last we'll set a buy limit
        - cancel old limit if exists
        - create new limit:
        -- If more buyers than sellers in order book set stop limit to + 1%

        :return:
        """
        if self.selling:
            return False

        last_sell = self.exchange_trader.last_sold_price
        if last_sell is 0:
            self.exchange_trader.last_sold = self.current_price

        if self.is_buy_condition(self.current_price, last_sell):
            stop_price, limit_price = self.exchange_trader.create_stop_limit_order(self.current_price, OrderAction.BUY)

        return True

    def make_sell_decision(self):
        """
        Check current price
        Check buy price
        If change in price greater than 1% set a sell limit:

        :return:
        """
        if self.buying:
            return False

    def is_buy_condition(self, current_price: float, last_sell: float):
        # Is the current price less than what we sold at
        if current_price > last_sell:
            return False

        # Has the price changed greater than 1%
        if not self.change_in_price_exceeds_threshold(current_price, last_sell, .001):
            return False

        if self.order_book_sell_dominant():
            return False

        return True

    def change_in_price_exceeds_threshold(self, current: float, last: float, threshold: float):
        """

        :param current:
        :param last:
        :param threshold: percent value of price change. 1.0 is 100%, .001 is 1%
        :return:
        """
        diff = abs(last-current)
        percent_change = diff / last
        return percent_change > threshold

    def order_book_sell_dominant(self):
        order_book = self.exchange_trader.order_book
        bid_info, ask_info = self.get_average_bid_ask(order_book)
        return ask_info['count'] > bid_info['count']

    def get_average_bid_ask(self, order_book: dict):
        bids = order_book['bids']
        asks = order_book['asks']
        bid_info = {
            'count': 0,
            'average_price': 0
        }
        ask_info = {
            'count': 0,
            'average_price': 0
        }
        for bid in bids:
            bid_info['count'] += bid[OrderBook.SIZE]
            bid_info['average_price'] += bid[OrderBook.PRICE]

        for ask in asks:
            ask_info['count'] += ask[OrderBook.SIZE]
            ask_info['average_price'] += ask[OrderBook.PRICE]

        bid_info['average_price'] = bid_info['average_price'] / bid_info['count']
        ask_info['average_price'] = ask_info['average_price'] / ask_info['count']

        return bid_info, ask_info

