from typing import List, Tuple


def get_seperate_data_list(data: List[list]) -> Tuple[list, list]:
    """
    :param data:
    :return: Tuple (list price data, list time data)
    """
    price_data = [v[1] for v in data]
    time_data = [v[0] for v in data]
    return price_data, time_data
