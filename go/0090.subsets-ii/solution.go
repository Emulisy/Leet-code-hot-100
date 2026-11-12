// https://leetcode.com/problems/subsets-ii/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func subsetsWithDup(nums []int) [][]int {
    res := [][]int{}
	for i := 0; i < len(nums); i++{
		for j := len(nums); j > i; j-- {
			res = append(res, nums[i : j])
		}
	}

	return res
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	nums := Deserialize[[]int](ReadLine(stdin))
	ans := subsetsWithDup(nums)
	fmt.Println("\noutput:", Serialize(ans))
}
