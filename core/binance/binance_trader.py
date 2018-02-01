import requests
from binance.client import Client

class BinanceTrader:

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError