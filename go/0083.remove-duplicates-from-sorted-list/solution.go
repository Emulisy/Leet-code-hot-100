// https://leetcode.com/problems/remove-duplicates-from-sorted-list/

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
	curr := head

	for curr != nil && curr.Next != nil {
		if curr.Val == curr.Next.Val {
			curr.Next = curr.Next.Next
		} else {
			curr = curr.Next
		}
	}

	return head
}

// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	head := Deserialize[*ListNode](ReadLine(stdin))
	ans := deleteDuplicates(head)
	fmt.Println("\noutput:", Serialize(ans))
}
