# https://leetcode.com/problems/regular-expression-matching/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution(object):
    def isMatch(self, text, pattern):
        memo = {}

        def dp(i, j):
            if (i, j) not in memo:
                if j == len(pattern):
                    ans = i == len(text)
                else:
                    first_match = i < len(text) and pattern[j] in {text[i], "."}
                    if j + 1 < len(pattern) and pattern[j + 1] == "*":
                        ans = dp(i, j + 2) or first_match and dp(i + 1, j)
                    else:
                        ans = first_match and dp(i + 1, j + 1)

                memo[i, j] = ans
            return memo[i, j]

        return dp(0, 0)

# @lc code=end

if __name__ == "__main__":
    s = json.loads(read_line())
    p = json.loads(read_line())
    ans = Solution().isMatch(s, p)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
