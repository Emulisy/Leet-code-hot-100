package LeetCode_Hot100

/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */

type ListNode struct {
    Val int
	Next *ListNode
 }

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