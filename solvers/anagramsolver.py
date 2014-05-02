import logging

from solvers.solver import IndicatorSolver
from solvers.solver import IndicatorType
from solution import Solution


class AnagramSolver(IndicatorSolver):
    """ A solver for anagram type clues.

    """

    def __init__(self, indicator_file, anagrammer):
        """
        :type anagrammer: anagrammer.Anagrammer
        :param indicator_file: str
        :param anagrammer:
        """
        IndicatorSolver.__init__(self, IndicatorType.anagram,
                                 indicator_file=indicator_file,
                                 anagrammer=anagrammer)
        logging.info("Initializing anagram solver")

    def get_solutions(self, clue):
        """ Get possible anagram type solutions to clue

        :rtype : list main.Solution
        :param clue: Clue to handle
        :return: List of solutions
        """
        logging.info("Getting anagram solutions")

        indicator_positions = \
            self.indicators.get_all_indicator_positions(clue.clue_words)

        # only check for valid subsets once
        if not indicator_positions:
            logging.info("No valid indicators")
            return []

        solns = []
        already_permuted = set([])

        letter_sets_to_permute = self.get_valid_length_combos(clue)
        logging.debug(str(letter_sets_to_permute))

        for (indices, letter_set) in letter_sets_to_permute:
            if letter_set in already_permuted:
                continue
            else:
                already_permuted.add("".join(sorted(letter_set)))

            logging.info("Permuting " + letter_set)
            anagrams = self.anagrammer.get_anagrams(letter_set)
            logging.info("Valid anagrams: " + str(anagrams))

            #todo: consider not having first for loop
            for indicator_pos in indicator_positions:
                for a in anagrams:
                    exclude = indices + [indicator_pos]
                    score = clue.check_definition(a, exclude)
                    if score > 0.0:
                        soln = Solution(a, score, clue_type=self.type,
                                        indicator=clue.terms[
                                            indicator_pos].word)
                        soln.add_note("Anagrammed from " + letter_set)
                        solns.append(soln)

        return solns

    # todo handle abbreviations
    def get_valid_length_combos(self, clue):
        """

        :rtype : list[str]
        """
        word_lengths = clue.word_lengths
        goal_length = clue.answer_length

        valid_subsets = self.get_subsets(0, goal_length, 0, word_lengths)

        letter_sets = []

        for index_set in valid_subsets:
            letter_set = ""
            for index in index_set:
                letter_set += clue.terms[index].word
            letter_sets.append((index_set, letter_set))

        return letter_sets

    def get_subsets(self, curr_len, goal_len, index, word_lengths):
        subsets = []
        for i in range(index, len(word_lengths)):
            word_len = word_lengths[i]
            if curr_len + word_len == goal_len:
                subsets.append([i])
            elif curr_len + word_len < goal_len:
                rest = self.get_subsets(curr_len + word_len, goal_len, i + 1,
                                        word_lengths)
                for s in rest:
                    subsets.append([i] + s)
        return subsets
