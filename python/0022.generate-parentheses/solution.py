# https://leetcode.com/problems/generate-parentheses/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        def dfs(op, cp, s):
            if op + cp == n * 2:
                res.append(s)
                return
            if op < n:
                dfs(op + 1, cp, s + '(')
            if cp < op:
                dfs(op, cp + 1, s + ')')
        dfs(0, 0, '')
        return res

# @lc code=end

if __name__ == "__main__":
    n = json.loads(read_line())
    ans = Solution().generateParenthesis(n)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
