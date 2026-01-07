import java.util.HashMap;

public class Solution45 {
//    使用dfs加memo复杂度是n**2 仍然会超时
//    public int jump(int[] nums) {
//        HashMap<Integer, Integer> memo = new HashMap<>();
//        dfs(nums, 0, 0, memo);
//        return memo.getOrDefault(nums.length - 1, Integer.MAX_VALUE);
//    }
//
//    private void dfs(int[] nums, int index, int steps, HashMap<Integer, Integer> memo) {
//        // 超出边界直接返回
//        if (index >= nums.length) return;
//
//        // 如果已经到终点，记录最少步数
//        if (index == nums.length - 1) {
//            memo.put(index, Math.min(memo.getOrDefault(index, Integer.MAX_VALUE), steps));
//            return;
//        }
//
//        // 如果已经走过，并且之前的步数更优，跳过
//        if (memo.containsKey(index) && memo.get(index) <= steps) return;
//
//        // 记录当前 index 所需最少步数
//        memo.put(index, steps);
//
//        // 尝试跳所有可能的步数
//        for (int jump = 1; jump <= nums[index]; jump++) {
//            dfs(nums, index + jump, steps + 1, memo);
//        }
//    }
//
//    public static void main(String[] args) {
//        Solution45 s = new Solution45();
//        System.out.println(s.jump(new int[]{2, 3, 1, 1, 4}));
//    }

    //所以只能使用贪心算法
    public int jump(int[] nums) {
        int jumps = 0;
        int farthest = 0;
        int end = 0;

        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == end) {
                jumps++;
                end = farthest;
            }
        }

        return jumps;
    }

    public static void main(String[] args) {
        Solution45 s = new Solution45();
        System.out.println(s.jump(new int[]{2, 3, 1, 1, 4}));
    }
}
