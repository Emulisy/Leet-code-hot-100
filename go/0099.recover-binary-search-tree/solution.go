// Created by Bob at 2026/11/21 14:59
// leetgo: dev
// https://leetcode.com/problems/recover-binary-search-tree/

package main

import (
	"bufio"
	"fmt"
	"os"

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
func recoverTree(root *TreeNode)  {
    var prev *TreeNode
    var first *TreeNode
    var second *TreeNode

    var inorder func(*TreeNode)

    inorder = func(node *TreeNode) {
        if node == nil {
            return
        }

        inorder(node.Left)

        // Compare prev with node here
        // Detect the two misplaced nodes
		if prev != nil && prev.Val > node.Val {
			if first == nil {
				first = prev
			}
			second = node
		}

        prev = node

        inorder(node.Right)
    }

    inorder(root)

    // Swap first.Val and second.Val
	tmp := first.Val
	first.Val = second.Val
	second.Val = tmp
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	recoverTree(root)
	ans := root

	fmt.Println("\noutput:", Serialize(ans))
}
