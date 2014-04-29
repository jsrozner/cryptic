from common import IndicatorDictionary
from enum import Enum

class IndicatorType(Enum):
    anagram = 1

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
        """
        self.type = type
        self.indicators = IndicatorDictionary(indicator_file)
        self.anagrammer = anagrammer
