# https://leetcode.com/problems/remove-nth-node-from-end-of-list/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

# Definition for singly-linked list.
from typing import Optional


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        left = head
        right = head
        overlay = n
        while True:
            if not right.next:#the end of the linkedlist
                if overlay: #if the left node never moved
                    if overlay == 1: #if the nth node from end is the head
                        head = head.next
                        return head
                    else:#if n > the length of the list
                        return None
                left.next = left.next.next
                return head
            if overlay:
                overlay = overlay - 1
            else:
                left = left.next
            right = right.next

# @lc code=end

if __name__ == "__main__":
    head = deserialize("ListNode", read_line())
    n = json.loads(read_line())
    ans = Solution().removeNthFromEnd(head, n)
    print("\noutput:", serialize(ans, "ListNode"))
