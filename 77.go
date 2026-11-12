package LeetCode_Hot100


func combine(n int, k int) [][]int {
	res := [][]int{}

	var backtrack func(start int, path []int)
	backtrack = func(start int, path []int) {
		if len(path) == k {
			// Make a copy of the current path and add it to the result
			pathCopy := make([]int, len(path))
			copy(pathCopy, path)
			res = append(res, pathCopy)
			return
		}
		for i := start; i <= n; i++ {
			path = append(path, i)
			backtrack(i+1, path)
			path = path[:len(path)-1] // Backtrack
		}
	}
	backtrack(1, []int{})
	return res
}