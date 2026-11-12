# https://leetcode.com/problems/longest-common-prefix/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        res = strs[0]
        for i in range(1 , len(strs)):
            res = res[:min(len(res), len(strs[i]))]
            for j in range(min(len(strs[i]), len(res))):
                if res[j] != strs[i][j]:
                    if j == 0 :
                        return ""
                    res = res[:j]
                    break
        return res

# @lc code=end

if __name__ == "__main__":
    strs = json.loads(read_line())
    ans = Solution().longestCommonPrefix(strs)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
