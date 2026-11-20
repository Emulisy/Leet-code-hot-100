// Created by Bob at 2026/11/18 23:02
// leetgo: dev
// https://leetcode.com/problems/binary-tree-inorder-traversal/

// @lc code=begin

import java.util.ArrayList;

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
class Solution {
     private void traverse(TreeNode node, List<Integer> res){
        if(node == null) {
            return;
        }
        traverse(node.left, res);
        res.add(node.val);
        traverse(node.right, res);
    }

    public List<Integer> inorderTraversal(TreeNode root) {
         ArrayList<Integer> res = new ArrayList<>();

         traverse(root, res);

         return res;
    }
}

// @lc code=end
