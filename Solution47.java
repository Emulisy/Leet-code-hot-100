import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Solution47 {
    public List<List<Integer>> permuteUnique(int[] nums) {
        ArrayList<List<Integer>> res = new ArrayList<List<Integer>>();
        HashMap<Integer, Integer> numMap = new HashMap<Integer, Integer>();
        for(int num : nums){
            numMap.put(num, numMap.getOrDefault(num, 0) + 1);
        }
        backTrack(new ArrayList<Integer>(), nums.length, res, numMap);
        return res;
    }

    public void backTrack(List<Integer> path, int totalLen, ArrayList<List<Integer>> res, HashMap<Integer, Integer> numMap) {
        if(path.size() == totalLen){
            res.add(new ArrayList<>(path));
            return;
        }
        for(int num : numMap.keySet()){
            if(numMap.get(num) <= 0){
                continue;
            }
            numMap.put(num, numMap.get(num) - 1);
            path.add(num);
            backTrack(path, totalLen, res, numMap);
            path.remove(path.size()-1);
            numMap.put(num, numMap.get(num) + 1);
        }
    }

    public static void main(String[] args) {
        Solution47 sol = new Solution47();
        int[] nums = {1,2,3};
        System.out.println(sol.permuteUnique(nums));
    }
}
