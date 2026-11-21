// Created by Bob at 2026/11/21 15:25
// leetgo: dev
// https://leetcode.com/problems/same-tree/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func isSameTree(p *TreeNode, q *TreeNode) bool {
    var traverse func(p *TreeNode, q *TreeNode) bool

	traverse = func(p *TreeNode, q *TreeNode) bool{
		if p == nil || q == nil{
			return p == q
		}

		if p.Val != q.Val{
			return false
		}else{
			return traverse(p.Left, q.Left) && traverse(p.Right, q.Right)
		}
	}

	return traverse(p, q)
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	p := Deserialize[*TreeNode](ReadLine(stdin))
	q := Deserialize[*TreeNode](ReadLine(stdin))
	ans := isSameTree(p, q)

	fmt.Println("\noutput:", Serialize(ans))
}
