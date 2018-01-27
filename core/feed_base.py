from abc import ABCMeta

ETH='ETH'
BTC='BTC'
USD='USD'


class FeedBase(object):
    __metaclass__ = ABCMeta

    @property
    def value(self):
        raise NotImplementedError

    def get_available_coins(cls):
        raise NotImplementedError