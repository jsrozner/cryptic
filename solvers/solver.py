from bisect import bisect_left
from difflib import get_close_matches
from enum import Enum

import logging

min_indicator_distance = 0.65

class IndicatorType(Enum):
    anagram = 1
    double = 2
    hidden = 3

class IndicatorSolver(object):
    """ Base class for indicator solvers

    :type indicator_file: str, A text file with indicator words
    :type anagrammer: anagrammer.Anagrammer
    """

    def __init__(self, type, indicator_file="", anagrammer=None):
        """

        :param indicator_file:
        :param anagrammer:
        :param type: IndicatorType
        :type anagrammer: anagrammer.Anagrammer
        """
        self.type = type
        if indicator_file != "":
            self.indicators = IndicatorDictionary(indicator_file)
        else:
            self.indcators = None
        self.anagrammer = anagrammer


class IndicatorDictionary:
    def __init__(self, indicator_file):
        """
        :type indicator_file: str
        """
        with open(indicator_file) as f:
            self.dict = [x.strip() for x in f.readlines()]
        logging.info("Opened indicator file %s" % indicator_file)

    def lookup(self, word):
        """ Get closest match to word (accepts imperfect matches)

        :param word: word to check in indicator dictionary
        :type word: str
        :return: closest match or None if none found
        :rtype: str
        """
        i = bisect_left(self.dict, word)
        match = get_close_matches(word, self.dict[i - 1:i + 1], n=1,
                                  cutoff=min_indicator_distance)
        if match:
            return match[0]
        else:
            return None
