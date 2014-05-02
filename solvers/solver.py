from bisect import bisect_left
from difflib import get_close_matches
from enum import Enum

import logging

min_indicator_distance = 0.75


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

        :param word: word to check in indicator dictionary
        :type word: str
        :return: closest match or None if none found
        :rtype: str
        """
        word = word_array[index]
        i = bisect_left(self.dict, word)
        nearest_matches = self.dict[i - 1: i + 1]

        # optimistically ignore subsequent words
        # todo: actually check further indicator
        # todo: return length of match as well
        for i in range(0, len(nearest_matches)):
            nearest_matches[i] = nearest_matches[i].split()[0]

        match = get_close_matches(word, nearest_matches, n=1,
                                  cutoff=min_indicator_distance)
        if match:
            logging.debug("Closest match to " + word + " is " + match[0])
            return match[0]
        else:
            return None

    def get_all_indicator_positions(self, word_array):
        """ Return positions of all indicator words

        :param list[str] word_array: Input word array
        :return: List of indicator position indices
        :rtype: list[int]
        """
        indicator_positions = []
        for i in range(0, len(word_array)):
            word = word_array[i]
            logging.debug("Looking for matching indicator: " + word)
            if self.lookup(i, word_array) is not None:
                logging.info("Got indicator: " + word)
                indicator_positions.append(i)
        return indicator_positions

