import java.util.*;

public class Solution39 {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates); // optional for early pruning
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
            if (candidates[i] > target) break; // pruning step

            path.add(candidates[i]);
            backtrack(candidates, target - candidates[i], i, path, res); // i, not i + 1 (reuse allowed)
            path.remove(path.size() - 1); // backtrack
        }
    }
}

