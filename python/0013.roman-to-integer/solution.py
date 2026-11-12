# https://leetcode.com/problems/roman-to-integer/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def romanToInt(self, s: str) -> int:
        res = 0
        roman = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        for a, b in zip(s, s[1:]):
            if roman[a] < roman[b]:
                res -= roman[a]
            else:
                res += roman[a]

        return res + roman[s[-1]]

# @lc code=end

if __name__ == "__main__":
    s = json.loads(read_line())
    ans = Solution().romanToInt(s)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
