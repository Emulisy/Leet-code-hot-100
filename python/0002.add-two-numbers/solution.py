# https://leetcode.com/problems/add-two-numbers/
import json
from typing import *
from leetgo_py import *

# @lc code=begin

class Solution(object):
    def turn_to_int(self, l1):
        digit = 1
        current = l1
        res = 0
        while True:
            res += current.val * digit
            if current.next is None:
                break
            current = current.next
            digit = digit * 10
        return res

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        n1 = self.turn_to_int(l1)
        n2 = self.turn_to_int(l2)
        res = str(n1 + n2)
        index = len(res) - 1
        head = ListNode(int(res[index]))
        current = head
        while True:
            if index < 0:
                break
            index -= 1
            current.next = ListNode(int(res[index]))
            current = current.next
        return head

# @lc code=end

if __name__ == "__main__":
    l1 = deserialize("ListNode", read_line())
    l2 = deserialize("ListNode", read_line())
    ans = Solution().addTwoNumbers(l1, l2)
    print("\noutput:", serialize(ans, "ListNode"))
