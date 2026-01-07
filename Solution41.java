import java.util.Arrays;
import java.util.HashSet;

public class Solution41 {
    public int firstMissingPositive(int[] nums) {
        Arrays.sort(nums);
        if (nums[nums.length - 1] <= 0) return 1;
        HashSet<Integer> set = new HashSet<>();
        for (int num : nums) {
            if (num <= 0) {
                continue;
            } else {
                set.add(num);
            }
        }
        for (int i = 1; i < nums[nums.length - 1]; i++) {
            if(!set.contains(i)){
                return i;
            }
        }
        return nums[nums.length - 1] + 1;
    }

    public int firstMissingPositive2(int[] nums) {
        int n = nums.length;

        // Step 1: 把无效数值（≤0 或 >n）替换成 n+1
        for (int i = 0; i < n; i++) {
            if (nums[i] <= 0 || nums[i] > n) {
                nums[i] = n + 1;
            }
        }

        // Step 2: 把出现在数组里的数对应下标标为负数
        for (int i = 0; i < n; i++) {
            int val = Math.abs(nums[i]);
            if (val <= n) {
                nums[val - 1] = -Math.abs(nums[val - 1]);
            }
        }

        // Step 3: 找第一个不是负数的位置
        for (int i = 0; i < n; i++) {
            if (nums[i] > 0) {
                return i + 1;
            }
        }

        // 如果所有 1 到 n 都存在，返回 n+1
        return n + 1;
    }
}
