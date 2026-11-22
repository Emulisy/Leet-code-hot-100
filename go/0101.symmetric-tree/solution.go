// Created by Bob at 2026/11/22 19:47
// leetgo: dev
// https://leetcode.com/problems/symmetric-tree/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func isSymmetric(root *TreeNode) bool {
    var checkOpposite func(p *TreeNode, q *TreeNode) bool
	checkOpposite = func(p *TreeNode, q *TreeNode) bool{
		if p == nil || q == nil{
			return p == q
		}

		if p.Val != q.Val{
			return false
		}

		return checkOpposite(p.Left, q.Right) && checkOpposite(p.Right, q.Left)
	}

	return checkOpposite(root.Left, root.Right)
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	ans := isSymmetric(root)

	fmt.Println("\noutput:", Serialize(ans))
}
