package LeetCode_Hot100

func plusOne(digits []int) []int {
	for i := len(digits) - 1; i >= 0; i-- {
		if digits[i] < 9 {
			digits[i]++
			return digits
		}

		digits[i] = 0
	}

	// Every digit was 9, for example [9, 9] -> [1, 0, 0]
	result := make([]int, len(digits)+1)
	result[0] = 1
	return result
}
