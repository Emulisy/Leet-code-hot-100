// https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/

package main

import (
	"bufio"
	"fmt"
	"os"
	. "github.com/j178/leetgo/testutils/go")

// @lc code=begin

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */

func deleteDuplicates(head *ListNode) *ListNode {
	dummy := &ListNode{Next: head}
	prev := dummy
	curr := head
	for curr != nil {
		if curr.Next != nil && curr.Val == curr.Next.Val {
			duplicateVal := curr.Val

			for curr != nil && curr.Val == duplicateVal {
				curr = curr.Next
			}

			prev.Next = curr
		} else {
			prev = curr
			curr = curr.Next
		}
	}
	return dummy.Next
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	head := Deserialize[*ListNode](ReadLine(stdin))
	ans := deleteDuplicates(head)
	fmt.Println("\noutput:", Serialize(ans))
}
