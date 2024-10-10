def find_longest(s):
  words = s.split()
  longest_word = max(words, key=len)
  return len(longest_word)
