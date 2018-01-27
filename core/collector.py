import requests

ETH='ETH'

class Collector:

   def __init__(self, feed):
      self.feed = feed

   def query_value(self, coin=ETH):
