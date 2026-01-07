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
