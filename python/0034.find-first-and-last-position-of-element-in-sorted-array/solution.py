# https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

from typing import List

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                l = r = mid
                # Expand to the left
                while l > 0 and nums[l - 1] == target:
                    l -= 1
                # Expand to the right
                while r < len(nums) - 1 and nums[r + 1] == target:
                    r += 1
                return [l, r]
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return [-1, -1]

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    target = json.loads(read_line())
    ans = Solution().searchRange(nums, target)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
