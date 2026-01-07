public class Solution38 {
    public String getRLE(String input) {
        if (input == null || input.isEmpty()) return "";

        StringBuilder res = new StringBuilder();
        int count = 1;

        for (int i = 1; i < input.length(); i++) {
            if (input.charAt(i) == input.charAt(i - 1)) {
                count++;
            } else {
                res.append(count).append(input.charAt(i - 1));
                count = 1;
            }
        }

        // Append last group
        res.append(count).append(input.charAt(input.length() - 1));
        return res.toString();
    }


    public String countAndSay(int n) {
        if (n == 1) return "1";
        else {
            return getRLE(countAndSay(n - 1));
        }
    }

    public static void main(String[] args) {
        Solution38 sol = new Solution38();
        System.out.println(sol.countAndSay(4));
    }
}
