class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        largest_len = 0 #largest length for now
        indexes = {}#store the char index pair
        start = 0 #store the start index of the current substring
        for i in range(len(s)):
            try: #if the char appeared before
                current_len = 0
                #if the char appeared in the current substring
                if indexes[s[i]] >= start:
                    current_len =  len(s[indexes[s[i]]:i])
                    start = indexes[s[i]] + 1
                elif indexes[s[i]] < start:
                    current_len = len(s[start:i + 1])
                if current_len > largest_len:
                    largest_len = current_len
                indexes[s[i]] = i
            except KeyError:
                indexes[s[i]] = i
                if len(s[start:i + 1]) > largest_len:
                    largest_len = len(s[start:i + 1])
        return largest_len
a = Solution()
print(Solution.lengthOfLongestSubstring(a,"bbtablud"))