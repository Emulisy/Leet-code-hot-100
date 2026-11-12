// https://leetcode.com/problems/valid-number/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

func isNumber(s string) bool {
	seenDigit := false
	seenDot := false
	seenExponent := false
	digitAfterExponent := true

	for i := 0; i < len(s); i++ {
		c := s[i]

		switch {
		case c >= '0' && c <= '9':
			seenDigit = true

			if seenExponent {
				digitAfterExponent = true
			}

		case c == '+' || c == '-':
			// A sign is allowed only:
			// 1. at the beginning
			// 2. immediately after e or E
			if i > 0 && s[i-1] != 'e' && s[i-1] != 'E' {
				return false
			}

		case c == '.':
			// Only one dot is allowed, and it cannot appear
			// inside the exponent.
			if seenDot || seenExponent {
				return false
			}

			seenDot = true

		case c == 'e' || c == 'E':
			// Only one exponent is allowed, and there must
			// already be a digit before it.
			if seenExponent || !seenDigit {
				return false
			}

			seenExponent = true
			digitAfterExponent = false

		default:
			return false
		}
	}

	return seenDigit && digitAfterExponent
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	s := Deserialize[string](ReadLine(stdin))
	ans := isNumber(s)
	fmt.Println("\noutput:", Serialize(ans))
}
