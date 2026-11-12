# Recommender systems are widely employed nowadays to suggest new books, movies, restaurants,
# etc that a user is likely to enjoy based on his past ratings. One commonly used technique is collaborative filtering,
# in which the recommender system tries to match your preferences with those of other users, and suggests items
# that got high ratings from users with similar tastes. A distance measure that can be used to analyse how similar
# the rankings of different users are is counting the number of inversions. The counting inversions problem is the
# following:
# 1
# • Input: An array V of n distinct integers.
# • Output: The number of inversions of V , i.e., the number of pairs of indices (i, j) such that i < j and V [i] >
# V [j].
# The exhaustive search algorithm for solving this problem has time complexity Θ(n ** 2). Describe an algorithm with
# time complexity O(n logn) for solving this problem.

def inversion(self, nums: [int]) -> int:
    def merge(l1: [int], l2: [int]):
        i, j = 0, 0
        res = []
        inv = 0
        while i < len(l1) and j < len(l2):
            if l1[i] < l2[j]:
                res.append(l1[i])
                i += 1
            elif l1[i] > l2[j]:
                res.append(l2[j])
                j += 1
                inv += 1

        while i < len(l1):
            res.append(l1[i])
            i += 1
        while j < len(l2):
            res.append(l2[j])
            j += 1

        return res, inv

    def count(arr: [int]):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2

        left, left_inv = count(arr[:mid])
        right, right_inv = count(arr[mid:])
        merged, merged_inv = merge(left, right)
        return merged, merged_inv + left_inv + right_inv

    temp, total_inv = count(nums)
    return total_inv


