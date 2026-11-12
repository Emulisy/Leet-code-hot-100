function merge(index1, index2, arr) {
    let merged = [
        Math.min(arr[index1][0], arr[index2][0]),
        Math.max(arr[index1][1], arr[index2][1])
    ];
    arr.splice(index1, 2, merged);
}

var insert = function(intervals, newInterval) {
    let left = 0;
    let right = intervals.length;

    // 二分找到插入位置
    while (left < right) {
        const mid = Math.floor((left + right) / 2);
        if(intervals[mid][0] < newInterval[0]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    intervals.splice(left, 0, newInterval);
    
    for (let i = 0; i < intervals.length - 1; i++) {
        if(intervals[i][1] >= intervals[i + 1][0]) {
            merge(i, i + 1, intervals);
            i--;
        }
    }

    return intervals;
};

