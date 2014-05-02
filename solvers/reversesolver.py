import logging

from lib import common
from solvers.solver import IndicatorSolver
from solvers.solver import IndicatorType
from solution import Solution


class ReverseSolver(IndicatorSolver):
    """ A solver for reversal type clues.

    """

    def __init__(self, indicator_file, anagrammer):
        """
        :param str indicator_file:
        :param anagrammer.Anagrammer anagrammer:
        """
        IndicatorSolver.__init__(self, IndicatorType.reverse,
                                 indicator_file=indicator_file,
                                 anagrammer=anagrammer)
        logging.info("Initializing reverse solver")

    def get_solutions(self, clue):
        """ Get possible reverse type solutions to clue


        :param clue.Clue clue: Clue to handle
        :return: List of solutions
        :rtype: list[solution.Solution]
        """
        logging.info("Getting reverse solutions")

        indicator_positions = \
            self.indicators.get_all_indicator_positions(clue.clue_words)

        if not indicator_positions:
            logging.debug("No valid indicators")
            return []

        solns = []
        # todo: consider not having first for loop
        for pos in indicator_positions:
            (valid, ignore) = \
                common.get_valid_surrounding_indices(pos, clue.clue_words)

            for index in valid:
                term = clue.terms[index]
                word = term.word
                logging.info('Checking reversal candidate ' + word)
                omit = ignore + [index]

                # todo: fix lines like this
                syns = term.syns[1]
                reversals = []
                for s in syns:
                    # todo: this shouldn't be necessary
                    s = s.split()[0]
                    if len(s) != clue.answer_length:
                        continue
                    rev = s[::-1]  # reverse the string
                    if self.anagrammer.is_word(rev):
                        score = clue.check_definition(rev, omit)
                        if score > 0.0:
                            soln = Solution(rev, score, clue_type=self.type,
                                            indicator=clue.clue_words[pos])
                            solns.append(soln)

        return solns

