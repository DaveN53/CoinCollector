from typing import Tuple

import numpy as np


class EMATrend:
    # EMA5 Less than other EMA
    BEAR = 1
    # EMA5 Greater than EMA26
    PARTIAL_BEAR = 2
    # EMA5 Greater than EMA26 and EMA50
    PARTIAL_BULL = 3
    # EMA5 Greater than other EMA
    BULL = 4


class TrendHelper:

    @staticmethod
    def ema_snapshot(price_data: []):

        return {
            'EMA5': TrendHelper.calculate_exponential_moving_average(price_data, 5.0),
            'EMA12': TrendHelper.calculate_exponential_moving_average(price_data, 12.0),
            'EMA26': TrendHelper.calculate_exponential_moving_average(price_data, 26.0),
            'EMA50': TrendHelper.calculate_exponential_moving_average(price_data, 50.0)
        }

    @staticmethod
    def calculate_simple_moving_average(candle_data: [], period: float):
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
        data_set = candle_data[-int(period):]
        for value in data_set:
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
    def calculate_moving_average_convergence_divergence(ema_12: list, ema_26: list) -> Tuple[list, list]:
        """
        Calculates macd + macd ema 9
        :param ema_12:
        :param ema_26:
        :return: Tuple (macd, macd ema 9)
        """
        ema_26_np = np.array(ema_26)
        ema_12_np = np.array(ema_12)

        macd_line = list(ema_12_np - ema_26_np)

        macd_data = []
        macd_ema_9 = []
        for idx, data in enumerate(macd_line):
            macd_data.append(data)
            try:
                macd_ema_9.append(TrendHelper.calculate_exponential_moving_average(macd_data[:idx], 9))
            except ValueError:
                pass

        return macd_line, macd_ema_9

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
