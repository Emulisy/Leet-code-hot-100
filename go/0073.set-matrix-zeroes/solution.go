// https://leetcode.com/problems/set-matrix-zeroes/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func setZeroes(matrix [][]int) {
	zero_r := make(map[int]bool)
	zero_c := make(map[int]bool)

	for i := 0; i < len(matrix); i++ {
		for j := 0; j < len(matrix[i]); j++ {
			if matrix[i][j] == 0 {
				zero_r[i] = true
				zero_c[j] = true
			}
		}
	}

	for row := range zero_r {
		for j := 0; j < len(matrix[row]); j++ {
			matrix[row][j] = 0
		}
	}

	for col := range zero_c {
		for i := 0; i < len(matrix); i++ {
			matrix[i][col] = 0
		}
	}
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	matrix := Deserialize[[][]int](ReadLine(stdin))
	setZeroes(matrix)
	ans := matrix
	fmt.Println("\noutput:", Serialize(ans))
}
