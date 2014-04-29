from common import IndicatorDictionary

kMinIndicatorDistance = 0.9


class IndicatorSolver(object):
    """

    :param indicator_file: A text file with indicator words
    :type anagrammer: anagrammer.Anagrammer
    """

    def __init__(self, indicator_file="", anagrammer=""):
        self.indicators = IndicatorDictionary(indicator_file)
        self.anagrammer = anagrammer
        print "indicator solver initialized"
