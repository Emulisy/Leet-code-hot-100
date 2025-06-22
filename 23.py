import heapq
from typing import Optional
from itertools import count

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        counter = count()  # Unique counter to avoid comparing ListNode

        # Initialize the heap with the head of each list
        for node in lists:
            if node:
                heapq.heappush(heap, (node.val, next(counter), node))

        dummy = ListNode(0)
        current = dummy

        while heap:
            val, _, node = heapq.heappop(heap)
            current.next = node
            current = current.next
            if node.next:
                heapq.heappush(heap, (node.next.val, next(counter), node.next))

        return dummy.next
