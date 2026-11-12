# https://leetcode.com/problems/remove-duplicates-from-sorted-array/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        left = 0
        while left < len(nums) - 1:
            if nums[left] == nums[left + 1]:
                del nums[left + 1]  # Don't move `left` yet
            else:
                left += 1
        return len(nums)  # Return new length

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    ans = Solution().removeDuplicates(nums)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
    print("mutated:", json.dumps(nums))
