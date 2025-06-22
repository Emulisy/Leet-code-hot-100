class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        keyTable = {"2": ["a", "b", "c"], "3": ["d", "e", "f"], "4": ["g", "h", "i"],
                    "5": ["j", "k", "l"], "6": ["m", "n", "o"], "7": ["p", "q", "r", "s"],
                    "8": ["t", "u", "v"], "9": ["w", "x", "y", "z"]
                    }
        if not digits:
            return []
        res = [""]
        while digits:
            temp = []
            for each_ in keyTable[digits[0]]:
                for each in res:
                    temp.append(each + each_)
            res = temp

            digits = digits[1:]
        return res

print(Solution().letterCombinations("23"))
print(Solution().letterCombinations("24"))



