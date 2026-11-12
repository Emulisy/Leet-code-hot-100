// https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func removeDuplicates(nums []int) int {
	count := 0
	index := 0

	for index < len(nums) {
		if index == 0 {
			count = 1
			index++
			continue
		}

		if nums[index] == nums[index-1] {
			count++

			if count > 2 {
				nums = append(nums[:index], nums[index+1:]...)
				count--
			} else {
				index++
			}
		} else {
			count = 1
			index++
		}
	}

	return len(nums)
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	nums := Deserialize[[]int](ReadLine(stdin))
	ans := removeDuplicates(nums)
	fmt.Println("\noutput:", Serialize(ans))
	fmt.Println("mutated:", Serialize(nums))
}
