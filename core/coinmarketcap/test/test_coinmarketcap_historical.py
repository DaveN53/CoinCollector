import os
import pytest
import logging
from core.coinmarketcap.coinmarketcap_historical import *

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

"""
Change ENV to 2.7. These will not work with ironpython env
:return:
"""

@pytest.fixture
def historical():
    cmc_historical =  CoinMarketCapHistorical()
    yield cmc_historical

def test_bnb_history(historical):
    result = historical.get_price_history(symbol='BNB', value='ETH')
    assert result

