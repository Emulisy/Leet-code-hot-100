/**
 * @param {number[]} nums
 * @return {number}
 */
var maxSubArray = function(nums) {
    let currentSum = nums[0];
    let maxSum = nums[0];
    for (let i = 1; i < nums.length; i++) {
        // 如果当前和加上 nums[i] 还不如单独 nums[i]，那就重开一段
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        // 更新最大值
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
};