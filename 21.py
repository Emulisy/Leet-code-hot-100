# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def compareLists(self, list1: ListNode, list2: ListNode) -> Optional[ListNode]:
        temp = None
        if list1.val <= list2.val:
            temp = list1
            list1 = list1.next
        else:
            temp = list2
            list2 = list2.next
        return temp

    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        head = None
        if list1.val <= list2.val:
            head = list1
            list1 = list1.next
        else:
            head = list2
            list2 = list2.next
        current = head
        while list1 and list2:
            current.next = self.compareLists(list1, list2)
            current = current.next
            if not list1:
                current.next = list2
                break
            elif not list2:
                current.next = list1
                break
        return head







