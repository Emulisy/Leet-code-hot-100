package LeetCode_Hot100

func fullJustify(words []string, maxWidth int) []string {
	addSpaces := func(n int) string {
		s := ""
		for i := 0; i < n; i++ {
			s += " "
		}
		return s
	}

	res := make([]string, 0)

	for len(words) > 0 {
		index := 0
		totalLen := 0

		for index < len(words) {
			if totalLen+len(words[index])+index > maxWidth {
				break
			}

			totalLen += len(words[index])
			index++
		}

		lineWords := words[:index]
		isLastLine := index == len(words)

		result := ""

		if isLastLine {
			for i, word := range lineWords {
				if i > 0 {
					result += " "
				}
				result += word
			}

			result += addSpaces(maxWidth - len(result))

		} else if len(lineWords) == 1 {
			result = lineWords[0]
			result += addSpaces(maxWidth - len(result))

		} else {
			totalSpaces := maxWidth - totalLen
			gaps := len(lineWords) - 1

			base := totalSpaces / gaps
			extra := totalSpaces % gaps

			for i, word := range lineWords {
				result += word

				if i < gaps {
					spaces := base

					if i < extra {
						spaces++
					}

					result += addSpaces(spaces)
				}
			}
		}

		res = append(res, result)

		words = words[index:]
	}

	return res
}
