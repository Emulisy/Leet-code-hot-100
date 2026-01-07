import java.util.ArrayList;
import java.util.List;

public class Solution51 {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        boolean[][] boolGrid = new boolean[n][n];

        // Initialize all cells to true
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                boolGrid[i][j] = true;
            }
        }

        auxiliarySolution(0, res, boolGrid, new ArrayList<>());
        return res;
    }

    public void auxiliarySolution(int row, List<List<String>> res, boolean[][] boolGrid, List<String> solution) {
        int n = boolGrid.length;
        if (row == n) {
            res.add(new ArrayList<>(solution));
            return;
        }
        for (int col = 0; col < n; col++) {
            if (boolGrid[row][col]) {
                StringBuilder rowSolution = new StringBuilder();
                for (int j = 0; j < n; j++) {
                    rowSolution.append(j == col ? "Q" : ".");
                }
                solution.add(rowSolution.toString());
                auxiliarySolution(row + 1, res, flip(boolGrid, row, col), solution);
                solution.removeLast();
            }
        }
    }


    public boolean[][] flip(boolean[][] board, int row, int col) {
        int n = board.length;
        boolean[][] res = new boolean[n][n];

        // Copy
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                res[i][j] = board[i][j];
            }
        }

        // Row & col
        for (int i = 0; i < n; i++) {
            res[row][i] = false;
            res[i][col] = false;
        }

        // Diagonals
        for (int i = -n; i <= n; i++) {
            int r = row + i;
            int c = col + i;
            if (r >= 0 && r < n && c >= 0 && c < n) res[r][c] = false;
        }
        for (int i = -n; i <= n; i++) {
            int r = row + i;
            int c = col - i;
            if (r >= 0 && r < n && c >= 0 && c < n) res[r][c] = false;
        }

        return res;
    }

    public static void main(String[] args) {
        Solution51 s = new Solution51();
        List<List<String>> solutions = s.solveNQueens(5);
        for (List<String> sol : solutions) {
            for (String row : sol) {
                System.out.println(row);
            }
            System.out.println();
        }
    }
}
