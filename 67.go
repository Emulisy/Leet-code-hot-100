package LeetCode_Hot100

func addBinary(a string, b string) string {
	i := len(a) - 1
	j := len(b) - 1
	carry := 0

	result := make([]byte, 0, max(len(a), len(b))+1)

	for i >= 0 || j >= 0 || carry > 0 {
		sum := carry

		if i >= 0 {
			sum += int(a[i] - '0')
			i--
		}

		if j >= 0 {
			sum += int(b[j] - '0')
			j--
		}

		digit := sum % 2
		carry = sum / 2

		result = append(result, byte(digit)+'0')
	}

	reverseBytes(result)

	return string(result)
}

func reverseBytes(values []byte) {
	left := 0
	right := len(values) - 1

	for left < right {
		values[left], values[right] = values[right], values[left]
		left++
		right--
	}
}
