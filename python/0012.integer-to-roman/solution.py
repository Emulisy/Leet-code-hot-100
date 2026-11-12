# https://leetcode.com/problems/integer-to-roman/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def intToRoman(self, num: int) -> str:
        value_symbols = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
            (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

        res = []

        for value, symbol in value_symbols:
            if num == 0:
                break
            count = num // value
            res.append(symbol * count)
            num -= count * value

        return ''.join(res)

# @lc code=end

if __name__ == "__main__":
    num = json.loads(read_line())
    ans = Solution().intToRoman(num)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
