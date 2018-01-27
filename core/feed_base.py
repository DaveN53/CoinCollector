from abc import ABCMeta

ETH='ETH'
BTC='BTC'
USD='USD'

class FeedBase(ABCMeta):

    def get_value(cls, coin):
        raise NotImplementedError

    def get_coins(cls):
        raise NotImplementedError