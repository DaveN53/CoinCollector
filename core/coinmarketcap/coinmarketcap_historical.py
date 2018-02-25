import requests
import json

class CoinMarketCapHistorical:

    BASE_URL = 'https://graphs2.coinmarketcap.com/currencies/'
    currencies = {
        'BNB': 'binance-coin',
        'ETH': 'ethereum'
    }

    values = {
        'BTC': 'price_btc',
        'ETH': 'price_platform',
        'USD': 'price_usd'
    }

    def get_historical_data(self, symbol='ETH'):
        currency = self.currencies[symbol]
        url = self.BASE_URL + currency

        response = requests.get(url)
        return response

    def get_price_history(self, symbol='BNB', value='USD'):
        """
        :param symbol:
        :param value: ETH, BTC, USD
        :return:
        """
        price_json = []
        response = self.get_historical_data(symbol=symbol)
        if response.ok:
            value = self.values[value]

            response_json = json.loads(response.text)
            if value in response_json:
                price_json = response_json[value]
        return price_json
