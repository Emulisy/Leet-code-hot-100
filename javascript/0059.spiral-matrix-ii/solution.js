/**
 * @param {number} n
 * @return {number[][]}
 */
var generateMatrix = function(n) {
    const row = n;

    const result = []
    for (let j = 0; j < row; j++) {
        result.push([]);
    }

    let top = 0;
    let bottom = row - 1;
    let left = 0;
    let right = row - 1;

    let num = 1;

    while(left <= right && top <= bottom) {
        for(let colTop = left; colTop <= right; colTop++) {
            result[top][colTop] = num;
            num ++;
        }
        top++;

        for(let rowRight = top; rowRight <= bottom; rowRight++) {
            result[rowRight][right] = num;
            num ++;
        }
        right--;

        for(let colBottom = right; colBottom >= left; colBottom--) {
            result[bottom][colBottom] = num;
            num ++;
        }
        bottom--;

        for(let rowLeft = bottom; rowLeft >= top; rowLeft--) {
            result[rowLeft][left] = num;
            num ++;
        }
        left++;
    }
    return result;
};