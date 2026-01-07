import java.util.*;

public class Solution40 {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates); // 必须排序以便去重
        List<List<Integer>> res = new ArrayList<>();
        backtrack(candidates, target, 0, new ArrayList<>(), res);
        return res;
    }

    private void backtrack(int[] candidates, int target, int startIndex, List<Integer> path, List<List<Integer>> res) {
        if (target == 0) {
            res.add(new ArrayList<>(path));
            return;
        }

        for (int i = startIndex; i < candidates.length; i++) {
            if (i > startIndex && candidates[i] == candidates[i - 1]) continue; // 跳过同一层重复的数

            if (candidates[i] > target) break; // 剪枝

            path.add(candidates[i]);
            backtrack(candidates, target - candidates[i], i + 1, path, res); // i+1 表示不能重复使用
            path.remove(path.size() - 1);
        }
    }
}
