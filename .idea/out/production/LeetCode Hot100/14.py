class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        res = strs[0]
        for i in range(1 , len(strs)):
            res = res[:min(len(res), len(strs[i]))]
            for j in range(min(len(strs[i]), len(res))):
                if res[j] != strs[i][j]:
                    if j == 0 :
                        return ""
                    res = res[:j]
                    break
        return res


