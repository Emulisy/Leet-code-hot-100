# https://leetcode.com/problems/merge-k-sorted-lists/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

import heapq
from typing import Optional
from itertools import count


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

# @lc code=end

if __name__ == "__main__":
    lists = deserialize("List[ListNode]", read_line())
    ans = Solution().mergeKLists(lists)
    print("\noutput:", serialize(ans, "ListNode"))
