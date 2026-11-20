// Created by Bob at 2026/11/20 16:19
// leetgo: dev
// https://leetcode.com/problems/interleaving-string/

package main

import (
	"bufio"
	"fmt"
	"os"

	. "github.com/j178/leetgo/testutils/go"
)

// @lc code=begin

// func dp(s1 string, s2 string, s3 string, isS1 bool) bool{
// 	res := false
// 	if len(s1) == 0 && len(s2) == 0 && len(s3) == 0{
// 		res = true
// 	}else{
// 		i := 0
// 		if isS1{
// 			for(i < len(s1) && i < len(s3)){
// 				if(s1[i] != s3[i]){
// 					break
// 				}
// 				if dp(s1[i+1:], s2, s3[i+1:], false){
// 					res = true
// 					break
// 				}
// 				i++
// 			}
// 		}else{
// 			for(i < len(s2) && i < len(s3)){
// 				if(s2[i] != s3[i]){
// 					break
// 				}
// 				if dp(s1, s2[i+1:], s3[i+1:], true) {
// 					res = true
// 					break
// 				}
// 				i++
// 			}
// 		}
// }
// 	return res
// }

func isInterleave(s1, s2, s3 string) bool {
    if len(s1)+len(s2) != len(s3) {
        return false
    }

    memo := make(map[[2]int]bool)
    visited := make(map[[2]int]bool)

    var dp func(i, j int) bool

    dp = func(i, j int) bool {
        key := [2]int{i, j}

        if visited[key] {
            return memo[key]
        }

        if i+j == len(s3) {
            return true
        }

        res := false

        if i < len(s1) && s1[i] == s3[i+j] {
            res = dp(i+1, j)
        }

        if !res && j < len(s2) && s2[j] == s3[i+j] {
            res = dp(i, j+1)
        }

        visited[key] = true
        memo[key] = res

        return res
    }

    return dp(0, 0)
}



// @lc code=end

func main() {
	stdin := bufio.NewReader(os.Stdin)
	s1 := Deserialize[string](ReadLine(stdin))
	s2 := Deserialize[string](ReadLine(stdin))
	s3 := Deserialize[string](ReadLine(stdin))
	ans := isInterleave(s1, s2, s3)

	fmt.Println("\noutput:", Serialize(ans))
}
