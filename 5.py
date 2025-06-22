class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        n = len(s)
        if n == 0:
            return ""

        """
        using dynamic programming
        """

        start = 0
        max_len = 1

        dp = [[False] * n for _ in range(n)] #initially all in table is False

        for i in range(n):
            dp[i][i] = True #one letter itself is a palindrome

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1

                if s[i] == s[j]:
                    if length == 2:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i + 1][j - 1]

                    if dp[i][j] and length > max_len:
                        start = i
                        max_len = length

        return s[start:start + max_len]
