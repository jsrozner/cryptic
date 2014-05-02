from bisect import bisect_left
from difflib import get_close_matches
from enum import Enum
from os.path import commonprefix

import logging

min_indicator_distance = 0.70


class IndicatorType(Enum):
    anagram = 1
    double = 2
    hidden = 3
    reverse = 4


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

    def __str__(self):
        return str(self.type)


# todo: should return indices of words to test
# todo: should return indices of words to ignore (part of indicator)
class IndicatorDictionary:
    def __init__(self, indicator_file):
        """
        :type indicator_file: str
        """
        with open(indicator_file) as f:
            self.dict = [x.strip() for x in f.readlines()]
        logging.info("Opened indicator file %s" % indicator_file)

    def lookup(self, index, word_array):
        """ Get closest match to word (accepts imperfect matches)

        :param list[str] word_array: str
        :param int index: index of word in word_array to check
        :return: closest match or None if none found
        :rtype: str
        """
        word = word_array[index]
        logging.debug("looking up in indicator dictionary: " + word)
        i = bisect_left(self.dict, word)
        nearest_matches = self.dict[i - 1: i + 1]

        # todo: return length of match as well
        for i in range(0, len(nearest_matches)):
            split = nearest_matches[i].split()
            # require multi-word indicators to match exactly
            # todo: after this, it's exact so don't use get_closest_matches
            if len(split) > 1 and \
                    not self.match_multiple_words(split, word_array[index:]):
                nearest_matches[i] = ""

        match = get_close_matches(word, nearest_matches, n=1,
                                  cutoff=min_indicator_distance)
        if not match:
            return None

        match = match[0]
        # todo: arbitrary, essentially checking stem of word
        if word != match and len(commonprefix([word, match])) < 3:
            return None

        logging.debug("Closest match to " + word + " is " + match)
        return match

    def match_multiple_words(self, indicator_array, word_array):
        for i in range(0, len(indicator_array)):
            if i >= len(word_array):
                return False
            if indicator_array[i] != word_array[i]:
                return False
        return True

    def get_all_indicator_positions(self, word_array):
        """ Return positions of all indicator words

        :param list[str] word_array: Input word array
        :return: List of indicator position indices
        :rtype: list[int]
        """
        indicator_positions = []
        for i in range(0, len(word_array)):
            word = word_array[i]
            if self.lookup(i, word_array) is not None:
                logging.info("Got indicator: " + word)
                indicator_positions.append(i)
        return indicator_positions

