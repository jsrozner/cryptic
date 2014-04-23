import string

def stripPunctuation(s):
  for c in string.punctuation:
    s.replace(c, "")
  return s

def startsWithUpperCase(s):
  return s[0].isUpper()
