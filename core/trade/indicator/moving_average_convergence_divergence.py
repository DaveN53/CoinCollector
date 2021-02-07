from typing import List, Optional

from core.trade.indicator.indicator import Indicator
from core.trend_helper import TrendHelper
from core.utilities import get_seperate_data_list


class MACD(Indicator):
    """
    https://www.investopedia.com/terms/m/macd.asp#:~:text=Moving%20average%20convergence%20divergence%20(MACD)%20is%20a%20trend%2Dfollowing,from%20the%2012%2Dperiod%20EMA.
    """

    def get_result(self, data: dict) -> float:

        ema_12, _ = get_seperate_data_list(data.get('ema12'))
        ema_26, _ = get_seperate_data_list(data.get('ema26'))

        macd_line, macd_ema_9 = TrendHelper.calculate_moving_average_convergence_divergence(ema_12, ema_26)
        crossed = self.check_cross(macd_line, macd_ema_9)

    @staticmethod
    def check_cross(macd: List[float], ema_9: List[float]) -> Optional[int]:
        """
        :param macd:
        :param ema_9:
        :return: (-1, 0, 1) 0 macd crosses to bottom (Bear), None no cross, 1 macd crosses to top (Bull)
        """
        last_two_macd = macd[-2:]
        last_two_ema_9 = ema_9[-2:]

        #  ema_9 below macd
        if last_two_ema_9[0] < last_two_macd[0]:
            # macd cross ema_9 to bottom
            if last_two_ema_9[1] > last_two_macd[1]:
                return 0
        else:
            if last_two_ema_9[1] < last_two_macd[1]:
                return 1
        return None
