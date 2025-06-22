class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        nums.sort()
        res = sum(nums[:3])  # Initialize to the sum of the first three numbers

        for i in range(len(nums) - 2):
            # Skip duplicates
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, len(nums) - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if abs(target - total) < abs(target - res):
                    res = total

                if total < target:
                    left += 1
                elif total > target:
                    right -= 1
                else:
                    # Exact match
                    return target

        return res
