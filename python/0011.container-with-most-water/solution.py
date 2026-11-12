# https://leetcode.com/problems/container-with-most-water/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        max_area = 0
        left, right = 0, len(height) - 1

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            if area > max_area:
                max_area = area

            if height[left] < height[right]:
                left += 1
            elif height[left] > height[right]:
                right -= 1
            else:
                # Move both if heights are equal to continue shrinking range
                left += 1
                right -= 1

        return max_area

# @lc code=end

if __name__ == "__main__":
    height = json.loads(read_line())
    ans = Solution().maxArea(height)
    print("\noutput:", json.dumps(ans, ensure_ascii=False, allow_nan=False))
