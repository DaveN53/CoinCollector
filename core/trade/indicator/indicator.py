class Indicator:

    def get_result(self, data: dict) -> float:
        """
        Return a value in the range 0 to 10 to indicate the result of analysis
        0 = Bear, 10 = Bull
        :return:
        """
        raise NotImplementedError