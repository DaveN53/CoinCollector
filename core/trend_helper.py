
class TrendHelper:
    @staticmethod
    def calculate_simple_moving_average( candle_data: {}, period: float):
        """
        calculate sma for the last point
        :param candle_data:
        :param period:
        :return:
        """
        if len(candle_data) < period:
            raise ValueError('Not enough data for period')

        return sum(candle_data[-int(period):]) / float(period)

    @staticmethod
    def calculate_exponential_moving_average(candle_data: [], period: float):
        """

        :param candle_data: list of price / close price
        :param period:
        :return:
        """
        if len(candle_data) < 2 * float(period):
            raise ValueError("data is too short")
        c = 2.0 / (float(period) + 1)
        current_ema = TrendHelper.calculate_simple_moving_average(
            candle_data[-int(period) * 2:-int(period)], int(period)
        )
        for value in candle_data[-int(period):]:
            current_ema = (c * value) + ((1 - c) * current_ema)
        return current_ema

    @staticmethod
    def calculate_smoothed_moving_average(candle_data: {}, smoothing_period: int = 12, shift_to_future: int = 5):
        """
        The first value of this smoothed moving average is calculated as the simple moving average (SMA):
        SUM1 = SUM (CLOSE (i), N)
        SMMA1 = SUM1 / N
        The second moving average is calculated according to this formula:
        SMMA (i) = (SMMA1*(N-1) + CLOSE (i)) / N
        Succeeding moving averages are calculated according to the below formula:
        PREVSUM = SMMA (i - 1) * N
        SMMA (i) = (PREVSUM - SMMA (i - 1) + CLOSE (i)) / N
        Where:
        SUM — sum;
        SUM1 — total sum of closing prices for N periods; it is counted from the previous bar;
        PREVSUM — smoothed sum of the previous bar;
        SMMA (i-1) — smoothed moving average of the previous bar;
        SMMA (i) — smoothed moving average of the current bar (except for the first one);
        CLOSE (i) — current close price;
        N — smoothing period.
        After arithmetic conversions the formula can be simplified:
        SMMA (i) = (SMMA (i - 1) * (N - 1) + CLOSE (i)) / N
        :param candle_data: data including median and close prices
        :param smoothing_period:
        :param shift_to_future:
        :return: list smoothed points
        """
        smma = []
        smma[0] = (candle_data[0]['close'] + smoothing_period) / smoothing_period
        smma[1] = (smma[0] * (smoothing_period - 1) + candle_data[1]['close']) / smoothing_period
        for i in range(2, len(candle_data)):
            prev_sum = smma[i - 1] * smoothing_period
            smma[i] = ((prev_sum - smma[i - 1]) + candle_data[i]['close']) / smoothing_period

        return smma

    @staticmethod
    def calculate_williams_alligator(candle_data: {}):
        """
        MEDIAN PRICE = (HIGH + LOW) / 2
        ALLIGATORS JAW = SMMA (MEDIAN PRICE, 13, 8)
        ALLIGATORS TEETH = SMMA (MEDIAN PRICE, 8, 5)
        ALLIGATORS LIPS = SMMA (MEDIAN PRICE, 5, 3)
        :param candle_data: dict containing High and Low prices
        :return:
        """
        for candle in candle_data:
            candle['median'] = (candle['high'] + candle['low']) / 2

        alligator_jaw = TrendHelper.calculate_smoothed_moving_average(candle_data, 13, 8)
        alligator_teeth = TrendHelper.calculate_smoothed_moving_average(candle_data, 8, 5)
        alligator_lips = TrendHelper.calculate_smoothed_moving_average(candle_data, 5, 3)

        raise NotImplementedError("implementation incomplete")