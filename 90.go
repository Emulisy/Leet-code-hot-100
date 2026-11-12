func subsetsWithDup(nums []int) [][]int {
    res := [][]int{}
	for i := 0; i < len(nums); i++{
		for j := len(nums); j > i; j-- {
			res = append(res, nums[i : j])
		}
	}

	return res
}