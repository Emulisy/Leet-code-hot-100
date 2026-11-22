// Created by Bob at 2026/11/22 19:51
// leetgo: dev
// https://leetcode.com/problems/binary-tree-level-order-traversal/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func levelOrder(root *TreeNode) (ans [][]int) {
	ans = [][]int{}

	if root == nil{
		return ans
	}

	ans = append(ans, []int{root.Val})
	
	var addLevel func(nodes []*TreeNode)

	addLevel = func(nodes []*TreeNode){
		nextLevel := []*TreeNode{}
		levelAns := []int{}
		for _, node := range(nodes){
			if node.Left != nil{
				levelAns = append(levelAns, node.Left.Val)
				nextLevel = append(nextLevel, node.Left)
			}
			if node.Right != nil{
				levelAns = append(levelAns, node.Right.Val)
				nextLevel = append(nextLevel, node.Right)
			}
		}
		if len(nextLevel) == 0{
			return
		}
		ans = append(ans, levelAns)
		addLevel(nextLevel)
	}
	
	addLevel([]*TreeNode{root})
	return ans
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	ans := levelOrder(root)

	fmt.Println("\noutput:", Serialize(ans))
}
