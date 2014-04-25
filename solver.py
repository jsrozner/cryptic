from bisect import bisect_left
from difflib import get_close_matches

from common import IndicatorDictionary

kMinIndicatorDistance = 0.9

class IndicatorSolver:
  def __init__(self, indicator_file):
    self.indicators = IndicatorDictionary(indicator_file)
    print "indicator solver initialized"





