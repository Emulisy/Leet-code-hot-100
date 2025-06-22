class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        res = []
        nums.sort()
        for i in range(len(nums) - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            num1 = nums[i]
            for j in range(i + 1, len(nums) - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:  # ✅ fix here
                    continue
                num2 = nums[j]
                left = j + 1
                right = len(nums) - 1

                while left < right:
                    foursum = num1 + num2 + nums[left] + nums[right]
                    if foursum == target:
                        res.append([num1, num2, nums[left], nums[right]])
                        left += 1
                        right -= 1

                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif foursum < target:
                        left += 1
                    else:
                        right -= 1
        return res
