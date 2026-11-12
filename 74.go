package LeetCode_Hot100

func biSearch(row []int, target int) bool {
	if len(row) < 1 {
		return false
	}

	mid := len(row) / 2

	if target == row[mid] {
		return true
	} else if target > row[mid] {
		return biSearch(row[mid+1:], target)
	} else {
		return biSearch(row[:mid], target)
	}
}

func searchMatrix(matrix [][]int, target int) bool {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return false
	}

	if target < matrix[0][0] ||
		target > matrix[len(matrix)-1][len(matrix[0])-1] {
		return false
	}

	var biRows func([][]int) bool

	biRows = func(newMatrix [][]int) bool {
		if len(newMatrix) < 1 {
			return false
		}

		mid := len(newMatrix) / 2
		row := newMatrix[mid]

		if target >= row[0] && target <= row[len(row)-1] {
			return biSearch(row, target)
		} else if target < row[0] {
			return biRows(newMatrix[:mid])
		} else {
			return biRows(newMatrix[mid+1:])
		}
	}

	return biRows(matrix)
}