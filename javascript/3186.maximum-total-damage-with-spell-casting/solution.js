/**
 * @param {number[]} power
 * @return {number}
 */
var maximumTotalDamage = function(power) {
    power.sort((a, b) => a - b); // ascend
    let count = 1;
    let merged = [];
    for (let i = 1; i < power.length; i++) {
        if (power[i] === power[i - 1]) {
            count++;
        } else {
            merged.push({ value: power[i - 1], count });
            count = 1;
        }
    }
    merged.push({ value: power[power.length - 1], count });

    let n = merged.length;
    let dp = Array(n).fill(0); // stores the largest total damage of the former spell values.
    dp[0] = merged[0].value * merged[0].count;

    for(let i = 1; i < n; i++) {
        let current = merged[i].value * merged[i].count;

        //find the last available spell value
        let j = i - 1;
        while(j >= 0 && merged[i].value - merged[j].value <= 2) {
            j--;
        }
        if(j >= 0){
            current += dp[j];
        }
        dp[i] = Math.max(current, dp[i - 1]);

    }
    return dp[n - 1];
};

console.log(maximumTotalDamage([1, 1, 3, 4]));
