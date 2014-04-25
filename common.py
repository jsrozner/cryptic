from bisect import bisect_left
from difflib import get_close_matches
from os.path import isfile

class IndicatorDictionary:
  kMinIndicatorDistance = 0.9
  def __init__(self, indicator_file):
    if isinstance(indicator_file, basestring):
      print "opened indicator file"
      with open(indicator_file) as f:
        self.dict = f.readlines()
    else:
      self.dict = indicator_file

  def lookup(self, word):
    i = bisect_left(self.dict, word)
    match = get_close_matches(word, self.dict[i-1:i+1], n=1,
                              cutoff=self.kMinIndicatorDistance)
    if match:
      return match[0]
    else:
      return None






