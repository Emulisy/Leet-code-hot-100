class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []
        def dfs(op, cp, s):
            if op + cp == n * 2:
                res.append(s)
                return
            if op < n:
                dfs(op + 1, cp, s + '(')
            if cp < op:
                dfs(op, cp + 1, s + ')')
        dfs(0, 0, '')
        return res

print(Solution().generateParenthesis(5))
