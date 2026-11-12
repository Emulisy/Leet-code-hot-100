# https://leetcode.com/problems/next-permutation/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        #wtf is this? garbage, u should at least tell me how the permutation goes
        i = len(nums) - 1
        while i > 0 and nums[i - 1] >= nums[i]:
            i -= 1

        if i == 0:
            nums.reverse()
            return

        j = len(nums) - 1
        while j >= i and nums[j] <= nums[i - 1]:
            j -= 1

        nums[i - 1], nums[j] = nums[j], nums[i - 1]

        nums[i:] = reversed(nums[i:])

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    Solution().nextPermutation(nums)
    ans = nums
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
