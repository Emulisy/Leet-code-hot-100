/**
 * @param {number[][]} intervals
 * @return {number[][]}
 */
var merge = function(intervals) {
    if (intervals.length === 0) return [];

    intervals.sort((a, b) => a[0] - b[0]);

    const res = [];
    let lastInterval = intervals[0];

    for (let i = 1; i < intervals.length; i++) {
        const curr = intervals[i];

        // overlap
        if (curr[0] <= lastInterval[1]) {
            lastInterval[1] = Math.max(lastInterval[1], curr[1]);
        }
        // no overlap
        else {
            res.push(lastInterval);
            lastInterval = curr;
        }
    }

    res.push(lastInterval);
    return res;
};
