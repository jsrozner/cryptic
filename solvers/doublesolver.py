from lib.common import get_syn_intersection
import logging

from solvers.solver import IndicatorSolver
from solvers.solver import IndicatorType
from solution import Solution

min_word_length = 3


class DoubleSolver(IndicatorSolver):
    """ A solver for hidden  type clues.

    """

    def __init__(self):
        """
        :type anagrammer: anagrammer.Anagrammer
        :param indicator_file: str
        :param anagrammer:
        """
        IndicatorSolver.__init__(self, IndicatorType.double)
        logging.info("Initializing double solver")

    def get_solutions(self, clue):
        """ Get possible double type solutions to clue


        :type clue: clue.Clue
        :rtype : list[main.Solution]
        :param clue: Clue to handle
        :return: List of solutions
        """
        logging.info("Getting double solutions")
        solns = []

        #todo: consider other split indices
        mid = len(clue.terms) / 2
        left = clue.terms[:mid]
        right = clue.terms[mid:]

        left_syns = []
        right_syns = []
        for term in left:
            if len(term.word) < min_word_length:
                continue
            left_syns += term.syns[1]
        for term in right:
            if len(term.word) < min_word_length:
                continue
            right_syns += term.syns[1]
        left_syns = set(left_syns)
        right_syns = set(left_syns)
        intersect = get_syn_intersection(left_syns, right_syns)
        valid = [w for w in intersect if len(w) == clue.answer_length]
        if len(valid) > 30:
            logging.warning("Too many double words to consider")
            return []
        for word in valid:
            if len(word) == clue.answer_length:
                logging.info('Checking double word ' + word)
                score = clue.check_definition(word)
                solns.append(Solution(word, score,
                                      clue_type=self.type))

        return solns

