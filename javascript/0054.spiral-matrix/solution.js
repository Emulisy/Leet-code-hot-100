/**
 * @param {number[][]} matrix
 * @return {number[]}
 */
var spiralOrder = function(matrix) {
    const res = [];

    function peel(mat) {
        if (!mat.length || !mat[0].length) return;

        res.push(...mat[0]);

        for (let i = 1; i < mat.length - 1; i++) {
            res.push(mat[i][mat[0].length - 1]);
        }

        if (mat.length > 1) {
            res.push(...mat[mat.length - 1].reverse());
        }

        if (mat[0].length > 1) {
            for (let i = mat.length - 2; i > 0; i--) {
                res.push(mat[i][0]);
            }
        }

        const inner = mat
            .slice(1, -1)
            .map(row => row.slice(1, -1));

        peel(inner);
    }

    peel(matrix);
    return res;
};
