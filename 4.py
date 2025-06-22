class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        if len(nums1) < len(nums2): return self.findMedianSortedArrays(nums2, nums1)
        n, m, tot, half, l, r = len(nums1), len(nums2), len(nums1) + len(nums2), (len(nums1) + len(nums2)) // 2, 0, len(
            nums2)
        while l <= r:
            i, j = (r + l) // 2, half - (r + l) // 2
            rightB, leftB = float('inf') if i == m else nums2[i], float('-inf') if i == 0 else nums2[i - 1]
            rightA, leftA = float('inf') if j == n else nums1[j], float('-inf') if j == 0 else nums1[j - 1]
            if leftB <= rightA and leftA <= rightB:
                return (min(rightA, rightB) + max(leftA, leftB)) / 2.0 if tot % 2 == 0 else min(rightA, rightB)
            if leftA > rightB:
                l = i + 1
            else:
                r = i - 1
        return -1
