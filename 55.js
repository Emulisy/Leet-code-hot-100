/**
 * @param {number[]} nums
 * @return {boolean}
 */
var canJump = function(nums) {
    maxReach = 0;

    for (let i = 0; i < nums.length; i++) {
        if(maxReach < i)  return false;

        maxReach  = Math.max(maxReach, nums[i] + i);

        if(maxReach >= nums.length - 1)  return true;
    }

    return true;

};