// Created by Bob at 2026/11/12 23:58
// leetgo: dev
// https://leetcode.com/problems/partition-list/

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
func partition(head *ListNode, x int) *ListNode {
    dummy := &ListNode{Next: head}
    left := dummy

    // Find the end of the initial partition (< x)
    for left.Next != nil && left.Next.Val < x {
        left = left.Next
    }

    right := left

    for right.Next != nil {
        if right.Next.Val >= x {
            right = right.Next
        } else {
            node := right.Next

            // Remove node from its current position
            right.Next = node.Next

            // Insert node after left
            node.Next = left.Next
            left.Next = node

            // Move left boundary forward
            left = node
        }
    }

    return dummy.Next
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	head := Deserialize[*ListNode](ReadLine(stdin))
	x := Deserialize[int](ReadLine(stdin))
	ans := partition(head, x)

	fmt.Println("\noutput:", Serialize(ans))
}
