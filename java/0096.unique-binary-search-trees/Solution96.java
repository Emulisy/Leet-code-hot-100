// Created by Bob at 2026/11/19 23:53
// leetgo: dev
// https://leetcode.com/problems/unique-binary-search-trees/

// @lc code=begin

class Solution96 {
    private int generate(int start, int end){
        if(start >= end){
            return 1;
        }else{
            int res = 0;
            for(int i = start; i <= end; i++){
                int leftNum = generate(start, i-1);
                int rightNum = generate(i+1, end);
                res += leftNum * rightNum;
            }
            return res;
        }
    }

    public int numTrees(int n) {
        return generate(1, n);
    }
}

// @lc code=end
