package LeetCode_Hot100

func subsets(nums []int) [][]int {
	res := [][]int{}
	path := []int{}

	var backtrack func(int)

	backtrack = func(start int) {
		// every path is a valid subset
		temp := append([]int{}, path...)
		res = append(res, temp)

		for i := start; i < len(nums); i++ {
			// choose nums[i]
			path = append(path, nums[i])

			// explore
			backtrack(i + 1)

			// undo choice
			path = path[:len(path)-1]
		}
	}

	backtrack(0)

	return res
}