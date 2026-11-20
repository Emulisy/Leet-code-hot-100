// Created by Bob at 2026/11/16 13:01
// leetgo: dev
// https://leetcode.com/problems/reverse-linked-list-ii/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reverseBetween(head *ListNode, left int, right int) (ans *ListNode) {
	if left < 1 || right < left {
		return nil
	}

	gap := right - left

	demo := &ListNode{Val: -1, Next: head}

	leftCount := 0
	revHead := demo //the node before left node
	var revTail *ListNode //the left node


	for(revHead.Next != nil){
		if leftCount < left - 1 {
			leftCount ++ 
			revHead = revHead.Next
			continue
		} else if leftCount == left - 1{
			revTail = revHead.Next
			break
		} 
	}

	for gap > 0 {
		tmp := revHead.Next
		revHead.Next = revTail.Next
		revTail.Next = revTail.Next.Next
		revHead.Next.Next = tmp
		gap -- 
	}

	return demo.Next
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	head := Deserialize[*ListNode](ReadLine(stdin))
	left := Deserialize[int](ReadLine(stdin))
	right := Deserialize[int](ReadLine(stdin))
	ans := reverseBetween(head, left, right)

	fmt.Println("\noutput:", Serialize(ans))
}
