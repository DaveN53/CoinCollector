from typing import List

from core.trade.indicator.indicator import Indicator


class EMACrossover(Indicator):

    def get_result(self, data: dict) -> float:
        """
        Return a value in the range -10 to 10 to indicate the result of analysis
        0 = Bear, 10 = Bull
        :return:
        """
        # TODO fine tune these cross signals because they're zero most of the time
        cross_5_12 = self.check_cross(slow_ema=data.get('ema12'), fast_ema=data.get('ema5'))
        cross_12_26 = self.check_cross(slow_ema=data.get('ema26'), fast_ema=data.get('ema12'))
        cross_5_50 = self.check_cross(slow_ema=data.get('ema50'), fast_ema=data.get('ema5'))

        pos_26_50 = self.check_position(slow_ema=data.get('ema50'), fast_ema=data.get('ema26'))
        pos_12_26 = self.check_position(slow_ema=data.get('ema26'), fast_ema=data.get('ema12'))
        pos_5_12 = self.check_position(slow_ema=data.get('ema12'), fast_ema=data.get('ema5'))

        print(f'cross_5_12: {cross_5_12}\ncross_12_26: {cross_12_26}\ncross_5_50: {cross_5_50}\n'
              f'pos_26_50: {pos_26_50}\npos_12_26: {pos_12_26}\npos_5_12: {pos_5_12}\n')

        result_data = [
            cross_5_12,
            cross_12_26,
            cross_5_50,
            pos_26_50,
            pos_12_26,
            pos_5_12
        ]
        result_data = list(filter(None, result_data))

        result_sum = float(sum(result_data))
        result_scaled = (result_sum / len(result_data)) * 10.0
        return result_scaled

    def check_cross(self, slow_ema: List[float], fast_ema: List[float]) -> int:
        """
        :param slow_ema:
        :param fast_ema:
        :return: (-1, 0, 1) -1 fast crosses to bottom (Bear), None no cross, 1 fast crosses to top (Bull)
        """
        last_two_slow = slow_ema[-2:]
        last_two_fast = fast_ema[-2:]

        # Slow below fast
        if last_two_slow[0] < last_two_fast[0]:
            # Top fast crossed slow to be bottom
            if last_two_slow[1] > last_two_fast[1]:
                return -1
        else:
            if last_two_slow[1] < last_two_fast[1]:
                return 1
        return None

    def check_position(self, slow_ema: List[float], fast_ema: List[float]) -> int:
        """
        :param slow_ema:
        :param fast_ema:
        :return: (-1, 1) -1 fast below slow (Bear), 1 fast above slow (Bull)
        """
        if slow_ema[-1] < fast_ema[-1]:
            return 1
        return -1
