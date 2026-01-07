import java.util.ArrayList;
import java.util.HashMap;

public class Solution36 {
    public boolean isValidSudoku(char[][] board) {
        HashMap<Character, ArrayList<int[]>> map = new HashMap<>();

        // Collect positions of each digit
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[0].length; j++) {
                char val = board[i][j];
                if (val != '.') {
                    map.putIfAbsent(val, new ArrayList<>());
                    map.get(val).add(new int[]{i, j});
                }
            }
        }

        // Validate each digit's positions
        for (char digit : map.keySet()) {
            ArrayList<int[]> positions = map.get(digit);
            int size = positions.size();
            for (int i = 0; i < size; i++) {
                int[] a = positions.get(i);
                for (int j = i + 1; j < size; j++) {
                    int[] b = positions.get(j);

                    // Same row
                    if (a[0] == b[0]) return false;

                    // Same column
                    if (a[1] == b[1]) return false;

                    // Same 3x3 box
                    if (a[0]/3 == b[0]/3 && a[1]/3 == b[1]/3) return false;
                }
            }
        }

        return true;
    }
}
