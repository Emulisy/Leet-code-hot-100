// Created by Bob at 2026/11/20 19:49
// leetgo: dev
// https://leetcode.com/problems/validate-binary-search-tree/

package main

import (
	"bufio"
	"fmt"
	"os"
	"math"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func isValidBST(root *TreeNode) bool {
    var dfs func(node *TreeNode, min, max *TreeNode)bool
	dfs = func(node *TreeNode, min, max *TreeNode)bool{
		if node == nil{
			return true
		}
		if min != nil && node.Left.Val >= min.Val{
			return false
		}
		if max != nil && node.Right.Val <= max.Val{
			return false
		}

		return dfs(node.Left, min, node) &&
               dfs(node.Right, node, max)
	}

	return dfs(root, nil, nil)
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	ans := isValidBST(root)

	fmt.Println("\noutput:", Serialize(ans))
}
