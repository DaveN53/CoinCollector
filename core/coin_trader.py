from core.binance.binance_trader import BinanceTrader


class CoinTrader:

    def __init__(self):
        self.binance_api_key = ''
        self.binance_api_secret = ''
        self.binance_trader = BinanceTrader()