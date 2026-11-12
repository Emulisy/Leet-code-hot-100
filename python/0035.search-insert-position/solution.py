# https://leetcode.com/problems/search-insert-position/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return left  # Insert position

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    target = json.loads(read_line())
    ans = Solution().searchInsert(nums, target)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
