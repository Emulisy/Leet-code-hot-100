// Created by Bob at 2026/11/13 16:09
// leetgo: dev
// https://leetcode.com/problems/decode-ways/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func numDecodings(s string) (ans int) {
	memo := make(map[string]int)
	return dp(s, memo)
}

func dp(s string, memo map[string]int) (int){
	if len(s) == 0 {
        return 1
    }

    if s[0] == '0' {
        return 0
    }

    if val, ok := memo[s]; ok {
        return val
    }

    count := dp(s[1:], memo)

    if len(s) >= 2 {
        n := int(s[0]-'0')*10 + int(s[1]-'0')

        if n <= 26 {
            count += dp(s[2:], memo)
        }
    }

    memo[s] = count
    return count
}


// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	s := Deserialize[string](ReadLine(stdin))
	ans := numDecodings(s)

	fmt.Println("\noutput:", Serialize(ans))
}
