package LeetCode_Hot100

import "strings"

// stack approach
func simplifyPath(path string) string {
	parts := strings.Split(path, "/")
	stack := []string{}

	for _, part := range parts {
		switch part {
		case "", ".":
			continue

		case "..":
			if len(stack) > 0 {
				stack = stack[:len(stack)-1]
			}

		default:
			stack = append(stack, part)
		}
	}

	return "/" + strings.Join(stack, "/")
}
