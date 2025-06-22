class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        y = str(abs(x))
        digit = 1
        res = 0
        for i in range(len(y)):
            res += int(y[i]) * digit
            digit *= 10
        if x < 0:
            res = -res
        if res < -2 ** 31 or res > 2 ** 31 - 1:
            return 0
        return res

