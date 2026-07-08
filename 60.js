var getPermutation = function(n, k) {
    let res = "";
    let nums = [];
    let fact = 1;

    for (let i = 1; i <= n; i++) {
        nums.push(i);
        fact *= i;
    }

    k--; // 转成 0-based

    for (let i = n; i >= 1; i--) {
        fact = fact / i;
        const index = Math.floor(k / fact);
        res += nums[index];
        nums.splice(index, 1);
        k = k % fact;
    }

    return res;
};

// 测试
console.log(getPermutation(4, 9)); // 输出 "2314"
