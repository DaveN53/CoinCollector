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
        graph_data = {'data': []}

        if coin_data:
            min_value = max_value = coin_data[0].value_market
            for coin in coin_data:
                if coin.value_market > max_value:
                    max_value = coin.value_market
                elif coin.value_market < min_value:
                    min_value = coin.value_market
                graph_data['data'].append([coin.date * 1000, coin.value_market])

            graph_data['min'] = min_value
            graph_data['max'] = max_value
            graph_data['num_labels'] = NUM_LABELS
        return graph_data

    def get_delete_time(self, time_period_hours=168):
        time_period_milli = time_period_hours * HOUR
        time_now = time.time()
        delete_time = time_now - time_period_milli
        return delete_time