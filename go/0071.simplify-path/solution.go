// https://leetcode.com/problems/simplify-path/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

import "strings"

// stack approach
func simplifyPath(path string) string {
	parts := strings.Split(path, "/")
	stack := []string{}

	for _, part := range parts {
		switch part {
		case "", ".":
			continue

		case "..":
			if len(stack) > 0 {
				stack = stack[:len(stack)-1]
			}

		default:
			stack = append(stack, part)
		}
	}

	return "/" + strings.Join(stack, "/")
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	path := Deserialize[string](ReadLine(stdin))
	ans := simplifyPath(path)
	fmt.Println("\noutput:", Serialize(ans))
}
