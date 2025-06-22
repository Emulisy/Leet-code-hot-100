class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]  # Base index for the first valid substring
        max_len = 0

        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)
            else:  # char == ')'
                stack.pop()
                if not stack:
                    stack.append(i)  # reset base
                else:
                    max_len = max(max_len, i - stack[-1])

        return max_len
