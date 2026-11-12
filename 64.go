package LeetCode_Hot100

func minPathSum(grid [][]int) int {
	m := len(grid)
	n := len(grid[0])

	minGrid := make([][]int, m)
	for i := 0; i < m; i++ {
		minGrid[i] = make([]int, n)
	}

	// Cost of reaching the starting cell.
	minGrid[0][0] = grid[0][0]

	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if i == 0 && j == 0 {
				continue
			}

			if i == 0 {
				// First row: can only come from the left.
				minGrid[i][j] = minGrid[i][j-1] + grid[i][j]
			} else if j == 0 {
				// First column: can only come from above.
				minGrid[i][j] = minGrid[i-1][j] + grid[i][j]
			} else {
				// Other cells: choose the cheaper previous path.
				minGrid[i][j] = min(
					minGrid[i-1][j],
					minGrid[i][j-1],
				) + grid[i][j]
			}
		}
	}

	return minGrid[m-1][n-1]
}
