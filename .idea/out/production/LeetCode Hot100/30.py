from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        ans = []
        if not words or not s:
            return ans

        word_len = len(words[0])
        word_count = len(words)
        total_len = word_len * word_count

        if len(s) < total_len:
            return ans

        # Frequency map of original words
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Iterate with sliding window starting at each offset
        for i in range(word_len):
            start = i
            matched_words = 0
            curr_freq = {}

            for j in range(i, len(s) - word_len + 1, word_len):
                curr_word = s[j:j + word_len]

                if curr_word in word_freq:
                    curr_freq[curr_word] = curr_freq.get(curr_word, 0) + 1
                    matched_words += 1

                    while curr_freq[curr_word] > word_freq[curr_word]:
                        left_word = s[start:start + word_len]
                        curr_freq[left_word] -= 1
                        start += word_len
                        matched_words -= 1

                    if matched_words == word_count:
                        ans.append(start)
                else:
                    curr_freq.clear()
                    matched_words = 0
                    start = j + word_len

        return ans
