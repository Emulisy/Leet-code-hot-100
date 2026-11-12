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
        count, temp = 0, head
        while temp and count < k:
            temp = temp.next
            count += 1
        if count < k:
            return head

        new_head = self.reverse(head, temp)
        head.next = self.reverseKGroup(temp, k)
        return new_head

# @lc code=end

if __name__ == "__main__":
    head = deserialize("ListNode", read_line())
    k = json.loads(read_line())
    ans = Solution().reverseKGroup(head, k)
    print("\noutput:", serialize(ans, "ListNode"))
