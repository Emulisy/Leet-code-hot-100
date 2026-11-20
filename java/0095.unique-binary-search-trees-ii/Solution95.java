// Created by Bob at 2026/11/19 19:16
// leetgo: dev
// https://leetcode.com/problems/unique-binary-search-trees-ii/

// @lc code=begin

import java.util.ArrayList;
import java.util.List;

import javax.swing.tree.TreeNode;

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution95 {

    private List<TreeNode> generate(int start, int end){
        List<TreeNode> res = new ArrayList<TreeNode>();
        if(start > end){
            res.add(null);
        }else if(start == end){
            res.add(new TreeNode(start));
        }else{
            for(int i = start; i <= end; i++){
                 List<TreeNode> leftAns = generate(start, i-1);
                 List<TreeNode> rightAns = generate(i+1, end);
                 for(TreeNode lTree : leftAns){
                    for(TreeNode rTree : rightAns){
                        TreeNode current = new TreeNode(i);
                        if(lTree == null){
                            current.left = null;
                        }else{
                            current.left = lTree;
                        }

                        if(rTree == null){
                            current.right = null;
                        }else{
                            current.right = rTree;
                        }   
                        res.add(current);
                    }
                 }
            }
        }
        return res;

    }

    public List<TreeNode> generateTrees(int n) {
         return generate(1, n);
    }
}

// @lc code=end
