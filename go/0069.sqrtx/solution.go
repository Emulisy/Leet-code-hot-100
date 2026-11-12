// https://leetcode.com/problems/sqrtx/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func mySqrt(x int) int {
	if x < 2 {
		return x
	}

	n := x
	guess := x

	for guess > n/guess {
		guess = (guess + n/guess) / 2
	}

	return guess
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	x := Deserialize[int](ReadLine(stdin))
	ans := mySqrt(x)
	fmt.Println("\noutput:", Serialize(ans))
}
