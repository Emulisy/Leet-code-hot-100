// https://leetcode.com/problems/subsets-ii/

package main

import (
	"bufio"
	"fmt"
	. "github.com/j178/leetgo/testutils/go"
	"os"
)

// @lc code=begin

import "sort"

func subsetsWithDup(nums []int) [][]int {
	values := append([]int{}, nums...)
	sort.Ints(values)
	res := [][]int{}
	path := []int{}

	var backtrack func(int)
	backtrack = func(start int) {
		res = append(res, append([]int{}, path...))
		for i := start; i < len(values); i++ {
			if i > start && values[i] == values[i-1] {
				continue
			}
			path = append(path, values[i])
			backtrack(i + 1)
			path = path[:len(path)-1]
		}
	}
	backtrack(0)

	return res
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	nums := Deserialize[[]int](ReadLine(stdin))
	ans := subsetsWithDup(nums)
	fmt.Println("\noutput:", Serialize(ans))
}
