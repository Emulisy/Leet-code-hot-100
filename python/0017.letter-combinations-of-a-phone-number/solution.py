# https://leetcode.com/problems/letter-combinations-of-a-phone-number/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        keyTable = {"2": ["a", "b", "c"], "3": ["d", "e", "f"], "4": ["g", "h", "i"],
                    "5": ["j", "k", "l"], "6": ["m", "n", "o"], "7": ["p", "q", "r", "s"],
                    "8": ["t", "u", "v"], "9": ["w", "x", "y", "z"]
                    }
        if not digits:
            return []
        res = [""]
        while digits:
            temp = []
            for each_ in keyTable[digits[0]]:
                for each in res:
                    temp.append(each + each_)
            res = temp

            digits = digits[1:]
        return res

# @lc code=end

if __name__ == "__main__":
    digits = json.loads(read_line())
    ans = Solution().letterCombinations(digits)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
