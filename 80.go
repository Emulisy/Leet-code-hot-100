package LeetCode_Hot100


func removeDuplicates(nums []int) int {
	count := 0
	index := 0

	for index < len(nums) {
		if index == 0 {
			count = 1
			index++
			continue
		}

		if nums[index] == nums[index-1] {
			count++

			if count > 2 {
				nums = append(nums[:index], nums[index+1:]...)
				count--
			} else {
				index++
			}
		} else {
			count = 1
			index++
		}
	}

	return len(nums)
}