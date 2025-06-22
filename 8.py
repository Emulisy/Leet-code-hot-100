class Solution(object):
    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        start_index = -1
        res = ""
        for i in range(len(s)):
            if s[i] == ' ':
                continue
            elif s[i] == '+' or '-' or s[i].isdigit():
                start_index = i
                res += s[i]
                break
            else:
                return 0
        if start_index == -1:
            return 0
        for j in range(start_index + 1, len(s)):
            if s[j].isdigit():
                res += s[j]
            else:
                break
        try:
            if int(res) < -2**31:
                return -2**31
            elif int(res) > 2**31 - 1:
                return 2**31 - 1
            return  int(res)
        except ValueError:
            return 0