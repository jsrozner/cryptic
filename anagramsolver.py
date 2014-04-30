import logging

from solver import IndicatorSolver
from solver import IndicatorType
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

    def get_anagram_solutions(self, clue):
        """ Get possible anagram type solutions to clue


        :rtype : list main.Solution
        :param clue: Clue to handle
        :return: List of solutions
        """
        logging.info("Getting anagram solutions")
        solns = []
        already_permuted = set([])

        for i in range(0, len(clue.terms)):
            term = clue.terms[i]
            logging.debug("Looking for matching indicator: " + term.word)
            if self.indicators.lookup(term.word) is not None:
                logging.info("Got indicator: " + term.word)

                letter_sets_to_permute = self.get_valid_length_combos(clue)

                for (indices, letter_set) in letter_sets_to_permute:
                    if letter_set in already_permuted:
                        continue
                    else:
                        already_permuted.add("".join(sorted(letter_set)))

                    logging.info("Permuting " + letter_set)
                    anagrams = self.anagrammer.getAnagrams(letter_set)
                    logging.info("Valid anagrams: " + str(anagrams))
                    for a in anagrams:
                        exclude = indices + [i]
                        score = clue.check_definition(a, exclude)
                        if score > 0.0:
                            soln =  Solution(a, score, clue_type=self.type,
                                             indicator=term.word)
                            soln.add_note("Anagrammed from " + letter_set)
                            solns.append(soln)

        return solns

    # todo: this function should pop out things like "with"
    # todo: handles only two word combos
    # todo: handle other comboes (remove clue word, parse "with", 3 words)
    # todo handle abbreviations
    def get_valid_length_combos(self, clue):
        """

        :rtype : list[str]
        """
        word_lengths = clue.word_lengths
        goal_length = clue.answer_length
        single_word_indices = []
        double_word_indices = []

        # Look over pairs of words only
        for i in range(0, len(word_lengths)):
            if (word_lengths[i] == goal_length):
                single_word_indices.append(i)
            elif i < len(word_lengths) - 1 \
                and word_lengths[i] + word_lengths[i + 1] == goal_length:
                double_word_indices.append(i)

        letter_sets = []

        for pos in single_word_indices:
            letter_sets.append(([pos], clue.terms[pos].word))
        for pos in double_word_indices:
            letter_sets.append(([pos, pos + 1],
                                clue.terms[pos].word + clue.terms[pos + 1].word))

        return letter_sets

