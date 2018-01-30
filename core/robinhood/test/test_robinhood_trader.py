import os
import pytest
import logging
from core.robinhood.robinhood_trader import *

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

"""
Change ENV to 2.7. These will not work with ironpython env
:return:
"""

@pytest.fixture
def trader():
    return RobinHoodTrader()

def test_robinhood_login(trader):
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    result = trader.login(username, password)
    assert result

def test_robinhood_logout(trader):
    result = trader.logout()
    assert result


