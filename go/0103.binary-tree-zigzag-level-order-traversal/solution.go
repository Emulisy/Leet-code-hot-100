// Created by Bob at 2026/11/23 15:40
// leetgo: dev
// https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/

package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

func zigzagLevelOrder(root *TreeNode) (ans [][]int) {
	ans = [][]int{}

	if root == nil{
		return ans
	}

	ans = append(ans, []int{root.Val})
	
	var addLevel func(nodes []*TreeNode, leftToRight bool)

	addLevel = func(nodes []*TreeNode, leftToRight bool){
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
		if(!leftToRight){
			slices.Reverse(levelAns)
		}
		ans = append(ans, levelAns)
		addLevel(nextLevel, !leftToRight)
	}
	
	addLevel([]*TreeNode{root}, false)
	return ans
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	root := Deserialize[*TreeNode](ReadLine(stdin))
	ans := zigzagLevelOrder(root)

	fmt.Println("\noutput:", Serialize(ans))
}
