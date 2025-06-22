class Solution(object):
    def find_remaining(self, first_line: list, second_line: list) -> int:
        chicken_num = first_line[1]
        while chicken_num >= second_line[0]:
            count = 0
            for i in range(len(second_line)):
                if second_line[i] > chicken_num:
                    break
                count += 1
            chicken_num -= count
        return chicken_num
print(Solution().find_remaining([4,5], [4,5,8,10]))
