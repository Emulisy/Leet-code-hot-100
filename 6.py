class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s

        result = []
        for i in range(numRows):
            result.append([])
        per_count = 2 * numRows - 2
        for i in range(len(s)):
            off_set = i % per_count
            if off_set < numRows:
                result[off_set].append(s[i])
            elif off_set >= numRows:
                off_set = off_set % numRows
                result[numRows - 2 - off_set].append(s[i])

        return_str = ''
        for each_row in result:
            for each_char in each_row:
                return_str += each_char

        return return_str

print(Solution().convert("PAYPALISHIRING", 4))



