// https://leetcode.com/problems/unique-paths-ii/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func uniquePathsWithObstacles(obstacleGrid [][]int) int {
	m := len(obstacleGrid) //the row count
	n := len(obstacleGrid[0])

	if obstacleGrid[0][0] == 1 || obstacleGrid[m-1][n-1] == 1 {
		return 0
	}

	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if obstacleGrid[i][j] == 1 {
				obstacleGrid[i][j] = -1
			}
		}
	}

	obstacleGrid[0][0] = 1

	var up func(i int, j int) int

	var left func(i int, j int) int

	up = func(i int, j int) int {
		if i == 0 {
			return 0
		} else {
			if obstacleGrid[i-1][j] < 0 {
				return 0
			} else {
				return obstacleGrid[i-1][j]
			}
		}
	}

	left = func(i int, j int) int {
		if j == 0 {
			return 0
		} else {
			if obstacleGrid[i][j-1] < 0 {
				return 0
			} else {
				return obstacleGrid[i][j-1]
			}
		}
	}

	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if obstacleGrid[i][j] < 0 {
				continue
			} else {
				obstacleGrid[i][j] += up(i, j) + left(i, j)
			}
		}
	}

	return obstacleGrid[m-1][n-1]
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	obstacleGrid := Deserialize[[][]int](ReadLine(stdin))
	ans := uniquePathsWithObstacles(obstacleGrid)
	fmt.Println("\noutput:", Serialize(ans))
}
