package LeetCode_Hot100

//this is O(MN) too slow
//func uniquePaths(m int, n int) int {
//	count := 0
//
//	var dp func(a int, b int)
//
//	dp = func(a int, b int) {
//		if a == m-1 && b == n-1 {
//			count++
//			return
//		}
//
//		if a >= m || b >= n {
//			return
//		}
//
//		dp(a+1, b)
//		dp(a, b+1)
//	}
//
//	dp(0, 0)
//	return count
//}

func uniquePaths(m int, n int) int {
	dp := make([]int, n)

	for i := 0; i < n; i++ {
		dp[i] = 1
	}

	for i := 1; i < m; i++ {
		for j := 1; j < n; j++ {
			dp[j] = dp[j] + dp[j-1]
		}
	}

	return dp[n-1]
}
