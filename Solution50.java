public class Solution50 {
    public double myPow(double x, int n) {
        long N = n; // 用 long 防止溢出
        if (N < 0) {
            x = 1 / x;
            N = -N;
        }
        return fastPow(x, N);
    }

    /**
     * @param x
     * @param n
     * @return
     * Instead of multiplying x once at a time, we multiply x ** (2/n) so that we
     * only iterate logN time, not N
     */
    private double fastPow(double x, long n) {
        if (n == 0) return 1.0; //base  case

        double half = fastPow(x, n / 2);
        if (n % 2 == 0) {
            return half * half;
        } else {
            return half * half * x;
        }
    }
}
