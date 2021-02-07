from typing import List, Optional

from core.trade.indicator.indicator import Indicator
from core.utilities import get_seperate_data_list


class EMACrossover(Indicator):

    def get_result(self, data: dict) -> float:
        """
        Return a value in the range 0 to 10 to indicate the result of analysis
        0 = Bear, 10 = Bull
        :return:
        """
        ema_5, _ = get_seperate_data_list(data.get('ema5'))
        ema_12, _ = get_seperate_data_list(data.get('ema12'))
        ema_26, _ = get_seperate_data_list(data.get('ema26'))
        ema_50, _ = get_seperate_data_list(data.get('ema50'))


        # TODO fine tune these cross signals because they're None most of the time
        cross_5_12 = self.check_cross(slow_ema=ema_12, fast_ema=ema_5)
        cross_12_26 = self.check_cross(slow_ema=ema_26, fast_ema=ema_12)
        cross_5_50 = self.check_cross(slow_ema=ema_50, fast_ema=ema_5)

        # TODO possibly add weights to these. 26_50 may not be necessary for action but should indicate absolute action
        pos_26_50 = self.check_position(slow_ema=ema_50, fast_ema=ema_26)
        pos_12_26 = self.check_position(slow_ema=ema_26, fast_ema=ema_12)
        pos_5_12 = self.check_position(slow_ema=ema_12, fast_ema=ema_5)

        result_data = [
            cross_5_12,
            cross_12_26,
            cross_5_50,
            pos_26_50,
            pos_12_26,
            pos_5_12
        ]
        result_data = [x for x in result_data if x is not None]
        result_sum = float(sum(result_data))
        result_scaled = (result_sum / len(result_data)) * 10.0
        return result_scaled

    def check_cross(self, slow_ema: List[float], fast_ema: List[float]) -> Optional[int]:
        """
        :param slow_ema:
        :param fast_ema:
        :return: (-1, 0, 1) 0 fast crosses to bottom (Bear), None no cross, 1 fast crosses to top (Bull)
        """
        last_two_slow = slow_ema[-2:]
        last_two_fast = fast_ema[-2:]

        # Slow below fast
        if last_two_slow[0] < last_two_fast[0]:
            # Top fast crossed slow to be bottom
            if last_two_slow[1] > last_two_fast[1]:
                return 0
        else:
            if last_two_slow[1] < last_two_fast[1]:
                return 1
        return None

    def check_position(self, slow_ema: List[float], fast_ema: List[float]) -> int:
        """
        :param slow_ema:
        :param fast_ema:
        :return: (-1, 1) 0 fast below slow (Bear), 1 fast above slow (Bull)
        """
        if slow_ema[-1] < fast_ema[-1]:
            return 1
        return 0
