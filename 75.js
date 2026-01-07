/**
 * @param {number[]} nums
 * @return {void} Do not return anything, modify nums in-place instead.
 */
var sortColors = function(nums) {
    let redNum = 0;
    let whiteNum = 0;
    function swap(i1, i2) {
        let temp = nums[i1];
        nums[i1] = nums[i2];
        nums[i2] = temp;
    }
    for(let i = 0; i < nums.length; i++){
        if(nums[i] === 0){
            swap(i, redNum);
            redNum++;
        }
    }
    for(let j = redNum; j < nums.length; j++){
        if(nums[j] === 1){
            swap(j, redNum + whiteNum);
            whiteNum++;
        }
    }
};
let nums = [2,0,2,1,1,0];
sortColors(nums);
console.log(nums);