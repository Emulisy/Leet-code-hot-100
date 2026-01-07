import java.util.HashMap;
import java.util.Map;

public class Solution44 {
    public boolean isMatch(String s, String p) {
        return match(s, p, 0, 0, new HashMap<>());
    }

    private boolean match(String s, String p, int i, int j, Map<String, Boolean> memo) {
        String key = i + "," + j;  //key to be stored in memo
        if (memo.containsKey(key)) return memo.get(key); //if already in memo, return it

        // Base case: pattern exhausted, which is string p is exhausted
        if (j == p.length()) {
            boolean res = i == s.length(); // s must also be exhausted
            memo.put(key, res);
            return res;
        }

        // If pattern has '*'
        if (p.charAt(j) == '*') {
            // Match zero or more characters
            boolean res = (i < s.length() && match(s, p, i + 1, j, memo)) || match(s, p, i, j + 1, memo);
            memo.put(key, res);
            return res;
        }

        // Match single character: if equal or '?'
        if (i < s.length() && (s.charAt(i) == p.charAt(j) || p.charAt(j) == '?')) {
            boolean res = match(s, p, i + 1, j + 1, memo);
            memo.put(key, res);
            return res;
        }

        // Otherwise, not match
        memo.put(key, false);
        return false;
    }
}
