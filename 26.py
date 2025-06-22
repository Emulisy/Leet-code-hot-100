class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        left = 0
        while left < len(nums) - 1:
            if nums[left] == nums[left + 1]:
                del nums[left + 1]  # Don't move `left` yet
            else:
                left += 1
        return len(nums)  # Return new length