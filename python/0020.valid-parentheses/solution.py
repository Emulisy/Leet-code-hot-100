# https://leetcode.com/problems/valid-parentheses/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        opening = {')': '(', ']': '[', '}': '{'}
        for each_char in s:
            if each_char in '([{':
                stack.append(each_char)
            elif each_char in opening:
                if not stack or stack.pop() != opening[each_char]:
                    return False
        return not stack

# @lc code=end

if __name__ == "__main__":
    s = json.loads(read_line())
    ans = Solution().isValid(s)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
