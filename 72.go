package LeetCode_Hot100

func minDistance(word1 string, word2 string) int {
	memo := make(map[[2]int]int) //for efficiency use memo + map

	var dp func(int, int) int

	dp = func(i, j int) int {
		if i == 0 {
			return j
		}
		if j == 0 {
			return i
		}

		key := [2]int{i, j}

		if value, exists := memo[key]; exists {
			return value
		}

		if word1[i-1] == word2[j-1] {
			memo[key] = dp(i-1, j-1)
		} else {
			delete := dp(i-1, j)
			insert := dp(i, j-1)
			replace := dp(i-1, j-1)

			memo[key] = min(delete, insert, replace) + 1
		}

		return memo[key]
	}

	return dp(len(word1), len(word2))
}
