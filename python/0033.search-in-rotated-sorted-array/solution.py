# https://leetcode.com/problems/search-in-rotated-sorted-array/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1

        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid

            # Left half is sorted
            if nums[low] <= nums[mid]:
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1

        return -1

# @lc code=end

if __name__ == "__main__":
    nums = json.loads(read_line())
    target = json.loads(read_line())
    ans = Solution().search(nums, target)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
