/**
 * @param {number} n
 * @return {number}
 */
//不用储存答案所以不需要复杂数据结构了
var totalNQueens = function(n) {
    let col = new Set();
    let diag1 = new Set(); //col + row
    let diag2 = new Set(); //col - row
    let res = 0;
    function backtracking(row){
        if(row === n){
            res++;
        }
        for(let i = 0; i < n; i++){
            if(col.has(i) || diag1.has(i + row) || diag2.has(i - row)){
                continue;
            }
            col.add(i);
            diag1.add(i + row);
            diag2.add(i - row);
            backtracking(row + 1);

            col.delete(i);
            diag1.delete(i + row);
            diag2.delete(i - row);
        }
    }
    backtracking(0);
    return res;
};