# https://leetcode.com/problems/reverse-nodes-in-k-group/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

# Definition for singly-linked list.
from typing import Optional


class Solution:
    def reverse(self, start, end):
        prev, curr = None, start
        while curr != end:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def reverseKGroup(self, head, k):
        if head is None or k == 1:
            return head

        dummy = ListNode(0)
        dummy.next = head
        previous = dummy
        while True:
            start = previous.next
            end = start
            for _ in range(k):
                if end is None:
                    return dummy.next
                end = end.next

            previous.next = self.reverse(start, end)
            start.next = end
            previous = start

# @lc code=end

if __name__ == "__main__":
    head = deserialize("ListNode", read_line())
    k = json.loads(read_line())
    ans = Solution().reverseKGroup(head, k)
    print("\noutput:", serialize(ans, "ListNode"))
