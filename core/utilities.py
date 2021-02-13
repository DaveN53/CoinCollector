from datetime import datetime
from typing import List, Tuple


def get_seperate_data_list(data: List[list]) -> Tuple[list, list]:
    """
    :param data:
    :return: Tuple (list price data, list time data)
    """
    price_data = [v[1] for v in data]
    time_data = [v[0] for v in data]
    return price_data, time_data


def get_hc_timestamp(date: datetime):
    """
    Get highcharts timestamp from datetime
    :param date:
    :return:
    """
    return date.timestamp() * 1000

def get_dt_hc(timestamp):
    """
    get datetime from highcharts timestamp
    :param timestamp:
    :return:
    """
    return datetime.fromtimestamp(timestamp / 1000)