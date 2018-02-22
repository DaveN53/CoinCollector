import time

HOUR = 3600
NUM_LABELS = 12

class DBHelper:

    def retrieve_graph_data_for_time_period(self, coin_data, period=24):
        """
        :param coin_data:
        :param period: time in hours
        :return:
        """
        interval = HOUR * period
        graph_data = {'labels': [], 'data': []}

        min_value = max_value = coin_data[0].value_market
        for coin in coin_data:

            value = coin.value_market
            if value > max_value:
                max_value = value
            elif value < min_value:
                min_value = value

            date_label = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(coin.date)
            )
            graph_data['labels'].append(date_label)
            graph_data['data'].append(value)

        graph_data['min'] = min_value
        graph_data['max'] = max_value
        graph_data['num_labels'] = NUM_LABELS
        return graph_data
