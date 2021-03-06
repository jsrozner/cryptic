import logging

from bisect import bisect_right
from collections import OrderedDict
from solvers.solver import IndicatorSolver
from solvers.solver import IndicatorType
from solution import Solution


class HiddenSolver(IndicatorSolver):
    """ A solver for hidden  type clues.

    """

    def __init__(self, indicator_file, anagrammer):
        """
        :type anagrammer: anagrammer.Anagrammer
        :param indicator_file: str
        :param anagrammer:
        """
        IndicatorSolver.__init__(self, IndicatorType.hidden,
                                 indicator_file=indicator_file,
                                 anagrammer=anagrammer)
        logging.info("Initializing hidden solver")

    def get_solutions(self, clue):
        """ Get possible hidden type solutions to clue


        :type clue: clue.Clue
        :rtype : list main.Solution
        :param clue: Clue to handle
        :return: List of solutions
        """
        logging.info("Getting hidden solutions")
        solns = []

        indicator_positions = \
            self.indicators.get_all_indicator_positions(clue.clue_words)

        if not indicator_positions:
            logging.debug("No valid indicators")
            return []

        # todo: consider not having first for loop
        for pos in indicator_positions:
            hidden_words = self.get_valid_letters(clue, pos, True)
            hidden_words += self.get_valid_letters(clue, pos, False)

            for (indices, word) in hidden_words:
                logging.info('Checking hidden word ' + word)
                omit = indices + [pos]
                score = clue.check_definition(word, omit)
                if score > 0.0:
                    soln = Solution(word, score, clue_type=self.type,
                                    indicator=clue.clue_words[pos])
                    solns.append(soln)

        return solns

    #todo: map character position to word index
    def get_valid_letters(self, clue, pos, get_left):
        """ pos specifies split index. get_left says get_left of the pos
        otherwise get right of it.

        :param clue:
        :param pos:
        :param get_left:
        :return:
        """
        valid_hidden_words = []
        full_string = ""
        length = 0
        pos_map = OrderedDict()

        r = range(0, pos)
        if not get_left:
            r = range(pos + 1, len(clue.terms))

        for i in r:
            # don't include indicator word
            if i == pos:
                continue
            word = clue.terms[i].word
            pos_map[length] = i
            full_string += word
            length += len(word)

        logging.info("Full string is: " + full_string)

        for i in range(0, len(full_string) - clue.answer_length):
            letters = full_string[i:i + clue.answer_length]
            if self.anagrammer.is_word(letters):
                # ignore exact word matches
                if i in pos_map.keys():
                    continue
                left_pos = bisect_right(pos_map.keys(), i)
                if left_pos == len(pos_map.keys()) or pos_map.keys()[left_pos] != i:
                    left_pos -= 1
                right_pos = bisect_right(pos_map.keys(),
                                         i + clue.answer_length - 1)
                if right_pos == len(pos_map.keys()) or pos_map.keys()[right_pos] != i + clue.answer_length - 1:
                    right_pos -= 1
                indices = [left_pos, right_pos]
                valid_hidden_words.append((indices, letters))

        return valid_hidden_words
