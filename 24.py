#Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def aux_swap(self, node: Optional[ListNode]) -> Optional[ListNode]:
        if node is None:
            return None
        current = node
        next_node = node.next
        try:
            current.next = self.aux_swap(next_node.next)
        except AttributeError:
            current.next = next_node.next
        next_node.next = current
        return next_node

    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        res = head.next
        self.aux_swap(head)
        return res



