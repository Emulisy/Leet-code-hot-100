import java.util.ArrayList;
import java.util.List;

public class Solution46 {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        backTrack(new ArrayList<>(), nums, res);
        return res;
    }

    public void backTrack(List<Integer> path, int[] nums, List<List<Integer>> res) {
        if(path.size() == nums.length){
            res.add(new ArrayList<>(path));
        }
        for(int i: nums){
            if(path.contains(i)){
                continue;
            }
            path.add(i);
            backTrack(path, nums, res);
            path.remove(path.size()-1);
        }
    }
}
