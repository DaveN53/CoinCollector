
class TradeRule:
    """
    Things to check out:
    Black–Scholes model
    k-nearest neighbors algorithm
    """

    def __int__(self, buy_threshold, sell_threshold):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def is_acceptable_buy(self, buy_rate_history, current_buy_rate):
        """
        Did we meet the threshold?
        Is the price trending up?
        Has the volume changed in a positive way?
        :param buy_rate_history: list of rate history 0 index is last known rate
        :param current_buy_rate:
        :return:
        """
        result = self.price_change_met_threshold(buy_rate_history, current_buy_rate)
        result = result & self.is_trending_up(buy_rate_history)
        result = result & self.is_acceptable_change_in_volume()

        return result

    def is_acceptable_change_in_volume(self):
        raise NotImplementedError

    def price_change_met_threshold(self, buy_rate_history, current_buy_rate):
        """
        :param buy_rate_history: list of rate history -1 index is last known rate (last added to list)
        :param current_buy_rate:
        :return:
        """
        last_low = self.get_last_low(buy_rate_history)
        if current_buy_rate < last_low:
            return False

        if current_buy_rate > last_low:
            diff = current_buy_rate - last_low
            thresh = diff / last_low
            if thresh > self.buy_threshold:
                return True

        return False

    def is_trending_up(self, rate_history):
        """
        Percent change for each:
        - Last low vs last high
        - Basement vs Ceiling
        - 30 min low vs 30 min high
        - 1hr low vs 1 hr high
        :param rate_history:
        :return:
        """
        raise NotImplementedError

    def is_acceptable_sell(self, last_buy_rate, current_buy_rate):
        difference = current_buy_rate - last_buy_rate
        if difference <= 0:
            return False

        percent_change = difference / last_buy_rate
        if percent_change > self.buy_threshold:
            return True

        return False

    def get_last_low(self, price_rate_history):
        low = price_rate_history[0]
        last_price = low
        for price in price_rate_history:
            if price > last_price:
                last_price = price
            else:
                low = price
                last_price = price
        return low

    def get_last_high(self, price_rate_history):
        high = price_rate_history[0]
        last_price = high
        for price in price_rate_history:
            if price < last_price:
                last_price = price
            else:
                high = price
                last_price = price
        return high

    def get_basement(self, price_rate_history):
        """
        Lowest price in local history
        :param price_rate_history:
        :return:
        """
        basement_price = price_rate_history[0]
        for price in price_rate_history:
            if price < basement_price:
                basement_price = price
        return basement_price

    def get_ceiling(self, price_rate_history):
        """
        Highest price in local history
        :param price_rate_history:
        :return:
        """
        ceiling_price = price_rate_history[0]
        for price in price_rate_history:
            if price > ceiling_price:
                ceiling_price = price
        return ceiling_price

