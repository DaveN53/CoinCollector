import logging
import os

import pytest

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

"""
Change ENV to 2.7. These will not work with ironpython env
:return:
"""

@pytest.fixture
def trader():
    rb_trader =  RobinHoodTrader()
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    result = rb_trader.login(username, password)
    log.info(result)
    yield rb_trader

    rb_trader.logout()

def test_watchlist(trader):
    result = trader.watchlist()
    assert result

def test_quote_eth(trader):
    result = trader.quote_data('ETH')
    assert result


