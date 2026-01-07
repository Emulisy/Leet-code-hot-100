class ListNode(object):
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
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
head = ListNode(2)
head.next = ListNode(4)
head.next.next = ListNode(3)
print(Solution().turn_to_int(head))