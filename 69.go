package LeetCode_Hot100

func mySqrt(x int) int {
	if x < 2 {
		return x
	}

	n := x
	guess := x

	for guess > n/guess {
		guess = (guess + n/guess) / 2
	}

	return guess
}
