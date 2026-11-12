# https://leetcode.com/problems/longest-valid-parentheses/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]  # Base index for the first valid substring
        max_len = 0

        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)
            else:  # char == ')'
                stack.pop()
                if not stack:
                    stack.append(i)  # reset base
                else:
                    max_len = max(max_len, i - stack[-1])

        return max_len

# @lc code=end

if __name__ == "__main__":
    s = json.loads(read_line())
    ans = Solution().longestValidParentheses(s)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
