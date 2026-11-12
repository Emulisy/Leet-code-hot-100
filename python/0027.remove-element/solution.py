# https://leetcode.com/problems/remove-element/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        index = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[index] = nums[i]
                index += 1
        return index

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    val = json.loads(read_line())
    ans = Solution().removeElement(nums, val)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
    print("mutated:", json.dumps(nums))
