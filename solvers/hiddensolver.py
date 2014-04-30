import logging

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
        """ Get possible anagram type solutions to clue


        :type clue: clue.Clue
        :rtype : list main.Solution
        :param clue: Clue to handle
        :return: List of solutions
        """
        logging.info("Getting hidden solutions")
        solns = []

        for i in range(0, len(clue.terms)):
            term = clue.terms[i]
            logging.debug("Looking for matching indicator: " + term.word)
            if self.indicators.lookup(term.word) is not None:
                logging.info("Got indicator: " + term.word)

                hidden_words = self.get_valid_letters(clue)

                for word in hidden_words:
                    logging.info('Checking hidden word ' + word)
                    score = clue.check_definition(word)
                    if score > 0.0:
                        soln = Solution(word, score, clue_type=self.type,
                                        indicator=term.word)
                        solns.append(soln)

        return solns

    #todo: map character position to word index
    def get_valid_letters(self, clue):
        valid_hidden_words = []
        full_string = ""
        for term in clue.terms:
            full_string += term.word
        logging.info("Full string is: " + full_string)

        for i in range(0, len(full_string) - clue.answer_length):
            letters = full_string[i:i + clue.answer_length]
            if self.anagrammer.isWord(letters):
                valid_hidden_words.append(letters)

        return valid_hidden_words
