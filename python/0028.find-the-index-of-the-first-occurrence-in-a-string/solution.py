# https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        for i in range(len(haystack)):
            try:
                if haystack[i:i+len(needle)] == needle:
                    return i
            except IndexError:
                pass
        return -1

# @lc code=end

if __name__ == "__main__":
    haystack = json.loads(read_line())
    needle = json.loads(read_line())
    ans = Solution().strStr(haystack, needle)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
