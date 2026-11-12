package LeetCode_Hot100

func climbStairs(n int) int {
	if n <= 0 {
		return 0
	}

	if n <= 2 {
		return n
	}

	prev2 := 1
	prev1 := 2

	for i := 3; i <= n; i++ {
		current := prev1 + prev2
		prev2 = prev1
		prev1 = current
	}

	return prev1
}
