// https://leetcode.com/problems/plus-one/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func plusOne(digits []int) []int {
	for i := len(digits) - 1; i >= 0; i-- {
		if digits[i] < 9 {
			digits[i]++
			return digits
		}

		digits[i] = 0
	}

	// Every digit was 9, for example [9, 9] -> [1, 0, 0]
	result := make([]int, len(digits)+1)
	result[0] = 1
	return result
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	digits := Deserialize[[]int](ReadLine(stdin))
	ans := plusOne(digits)
	fmt.Println("\noutput:", Serialize(ans))
}
