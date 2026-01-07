class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        for i in range(len(haystack)):
            try:
                if haystack[i:i+len(needle)] == needle:
                    return i
            except IndexError:
                pass
        return -1
            