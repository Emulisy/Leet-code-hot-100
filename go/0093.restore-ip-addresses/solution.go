// Created by Bob at 2026/11/18 20:12
// leetgo: dev
// https://leetcode.com/problems/restore-ip-addresses/

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"strconv"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func restoreIpAddresses(s string) (ans []string) {
    var backtrack func(prev []string, rest string)

    backtrack = func(prev []string, rest string) {
        if len(prev) == 4 {
            if len(rest) == 0 {
                ans = append(ans, strings.Join(prev, "."))
            }
            return
        }

        for i := 1; i <= 3; i++ {
            if i > len(rest) {
                break
            }

            if i > 1 && rest[0] == '0' {
                break
            }

            val, _ := strconv.Atoi(rest[:i])
            if val > 255 {
                break
            }

            // Choose
            prev = append(prev, rest[:i])

            // Explore
            backtrack(prev, rest[i:])

            // Undo
            prev = prev[:len(prev)-1]
        }
    }

    backtrack([]string{}, s)
    return ans
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	s := Deserialize[string](ReadLine(stdin))
	ans := restoreIpAddresses(s)

	fmt.Println("\noutput:", Serialize(ans))
}
