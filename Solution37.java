import java.util.*;

public class Solution37 {
    private final int SIZE = 9;
    private final int FULL_MASK = 0x1FF; // 9 bits: 111111111

    private int[] rows = new int[9];
    private int[] cols = new int[9];
    private int[] boxes = new int[9];
    private List<int[]> empties = new ArrayList<>();

    public void solveSudoku(char[][] board) {
        // Preprocess board: fill bitmasks and collect empty cells
        for (int r = 0; r < SIZE; r++) {
            for (int c = 0; c < SIZE; c++) {
                char ch = board[r][c];
                if (ch == '.') {
                    empties.add(new int[]{r, c});
                } else {
                    int digit = ch - '1';
                    setMask(r, c, digit, true);
                }
            }
        }
        dfs(board, 0);
    }

    private boolean dfs(char[][] board, int idx) {
        if (idx == empties.size()) return true;

        int[] pos = empties.get(idx);
        int r = pos[0], c = pos[1];
        int boxIdx = (r / 3) * 3 + (c / 3);
        int mask = rows[r] | cols[c] | boxes[boxIdx];
        for (int d = 0; d < SIZE; d++) {
            int bit = 1 << d;
            if ((mask & bit) == 0) {
                board[r][c] = (char) (d + '1');
                setMask(r, c, d, true);

                if (dfs(board, idx + 1)) return true;

                setMask(r, c, d, false);
                board[r][c] = '.';
            }
        }
        return false;
    }

    private void setMask(int r, int c, int d, boolean add) {
        int bit = 1 << d;
        if (add) {
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[(r / 3) * 3 + (c / 3)] |= bit;
        } else {
            rows[r] &= ~bit;
            cols[c] &= ~bit;
            boxes[(r / 3) * 3 + (c / 3)] &= ~bit;
        }
    }
}
