from typing import List

from core.trade.indicator.indicator import Indicator
from core.trend_helper import TrendHelper
from core.utilities import get_seperate_data_list


class MACD(Indicator):
    """
    https://www.investopedia.com/terms/m/macd.asp#:~:text=Moving%20average%20convergence%20divergence%20(MACD)%20is%20a%20trend%2Dfollowing,from%20the%2012%2Dperiod%20EMA.
    """

    def get_result(self, data: dict) -> List[float]:

        ema_12, _ = get_seperate_data_list(data.get('ema12'))
        ema_26, _ = get_seperate_data_list(data.get('ema26'))

        macd_line, macd_ema_9 = TrendHelper.calculate_moving_average_convergence_divergence(ema_12, ema_26)

        signal_crossed = self.check_signal_cross(macd_line, macd_ema_9)
        zero_line_crossed =self.zero_line_cross(macd_line)
        curr_momentum = self.current_momentum(macd_line)


        # If we don't have a cross don't bother checker other signals
        # if not signal_crossed:
        #     return []
        return [signal_crossed, zero_line_crossed, curr_momentum]


    @staticmethod
    def check_signal_cross(macd: List[float], ema_9: List[float]) -> float:
        """
        :param macd:
        :param ema_9:
        :return: (0, None, 1) -10 macd crosses to bottom (Bear), 0 no cross, 10 macd crosses to top (Bull)
        """
        last_two_macd = macd[-2:]
        last_two_ema_9 = ema_9[-2:]

        #  ema_9 below macd
        if last_two_ema_9[0] < last_two_macd[0]:
            # macd cross ema_9 to bottom
            if last_two_ema_9[1] > last_two_macd[1]:
                return -10.0
        else:
            if last_two_ema_9[1] < last_two_macd[1]:
                return 10.0
        return 0.0

    @staticmethod
    def zero_line_cross(macd: List[float]) -> float:

        # Bullish
        if macd[-2] < 0 < macd[-1]:
            return 10.0

        # Bearish
        if macd[-2] > 0 > macd[-1]:
            return -10.0

        return 0.0

    @staticmethod
    def current_momentum(macd: List[float]) -> float:
        """
        Return 1 if bullish, 0 if bearish
        :param macd:
        :return:
        """
        if macd[-1] > 0:
            return 10.0
        return -10.0
