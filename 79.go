package LeetCode_Hot100

func exist(board [][]byte, word string) bool {
	var dfs func(i, j, index int) bool

	dfs = func(i, j, index int) bool {
		if i < 0 || i >= len(board) ||
			j < 0 || j >= len(board[0]) {
			return false
		}

		if board[i][j] != word[index] {
			return false
		}

		if index == len(word)-1 {
			return true
		}

		temp := board[i][j]
		board[i][j] = '#'

		found :=
			dfs(i+1, j, index+1) ||
			dfs(i-1, j, index+1) ||
			dfs(i, j+1, index+1) ||
			dfs(i, j-1, index+1)

		board[i][j] = temp

		return found
	}

	for i := 0; i < len(board); i++ {
		for j := 0; j < len(board[i]); j++ {
			if dfs(i, j, 0) {
				return true
			}
		}
	}

	return false
}