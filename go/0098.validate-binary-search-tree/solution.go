// Created by Bob at 2026/11/20 19:49
// leetgo: dev
// https://leetcode.com/problems/validate-binary-search-tree/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func isValidBST(root *TreeNode) bool {
    
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	ans := isValidBST(root)

	fmt.Println("\noutput:", Serialize(ans))
}
