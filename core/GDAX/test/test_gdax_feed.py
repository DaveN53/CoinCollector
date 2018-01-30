import pytest
import logging
from core.GDAX.gdax_trader import *

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

"""
Change ENV to 2.7. These will not work with ironpython env
:return:
"""


@pytest.fixture
def gdax_f_man():
    return GDAXTrader()


def test_get_coins(gdax_f_man):
    gdax_f_man.get_available_coins()


def test_get_eth_value_usd(gdax_f_man):
    value = gdax_f_man.value
    assert value == 0


def test_get_info(gdax_f_man):
    info = gdax_f_man.get_coin_info()
    log.info(info)
    assert info
