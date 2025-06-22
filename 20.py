class Solution:
    def isValid(self, s: str) -> bool:
        temp1 = []
        temp2 = []
        temp3 = []
        for each_char in s:
            if each_char == '(':
                temp1.append(each_char)
            elif each_char == ')':
                if not temp1:
                    return False
                temp1.pop()
            elif each_char == '[':
                temp2.append(each_char)
            elif each_char == ']':
                if not temp2:
                    return False
                temp2.pop()
            elif each_char == '{':
                temp3.append(each_char)
            elif each_char == '}':
                if not temp3:
                    return False
                temp3.pop()
            else:
                continue
        return not temp1 and not temp2 and not temp3

