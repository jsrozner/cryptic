import logging

from lib import common, mystring
from thesaurus import thesaurus


class Term:
    """ Component of a clue.
    
    Attributes:
        is_upper_case: whether term initially started with upper case letter
        word: actual lower-cased word
        related_words: tuple of (syns, defs)
    
    """

    def __init__(self, word):
        """
        :param word: The initial word of the clue
        :type word: str
        """
        if mystring.starts_with_upper_case(word):
            self.is_upper_case = True
        else:
            self.is_upper_case = False

        self.word = word.lower()

        depth = 2
        self.related_words = common.get_related_words(self.word, depth)
        self.syns = thesaurus.get_synonyms(self.word, depth)
        logging.debug("Words related to " + self.word + " with depth " +
                      str(depth))


class Clue:
    """ Clue representation type

    Attributes:
        original_clue: the original string
        answer_length: the length specified by a number at the end of the clue
        word_lengths: lengths of all words in the clue after stripping
            punctuation
        terms: components of clue as clue.Term
        clue_words: components of clue as strings
        ends_with_question: if clue originally ended with question mark
        ends_with_exclamation: if clue originally ended with exclamation mark

    """
    # flags

    def __init__(self, input_clue):
        """

        :type input_clue: str
        """
        self.original_clue = input_clue

        self.ends_with_question = False
        self.ends_with_exclamation = False
        if input_clue[-1] == "?":
            self.ends_with_question = True
        elif input_clue[-1] == "!":
            self.ends_with_exclation = True

        # todo: consider removing punctuation post separation
        input_clue = mystring.strip_punctuation(input_clue)  # remove punctuation
        clue_words = input_clue.split()

        #todo: support (3,4) style
        try:
            self.answer_length = int(clue_words[-1])
        except:
            print("No length of input_clue given.")
            return

        clue_words = clue_words[0:-1]  # strip out length
        self.clue_words = clue_words
        self.word_lengths = map(len, clue_words)
        self.terms = map(Term, clue_words)

    def check_definition(self, soln, omit=[], split_in_half=True):
        """ Get a score for similarity

        :param soln: the tentative solution
        :type soln: str
        :param omit: indices of words in the clue to omit
        :type omit: list[int]
        :param split_in_half: whether to search only one side for definition
        :type split_in_half: bool
        :return: score
        :rtype: float
        """
        depth = 2
        soln_words = common.get_related_words(soln, depth)
        soln_syns = thesaurus.get_synonyms(soln, depth)

        last = len(self.terms) - 1
        omit = sorted(set(omit))

        term_range = range(0, last)  # default
        if omit and split_in_half:
            if 0 in omit and last in omit:
                return 0.0
            elif 0 in omit:
                term_range = range(omit[-1] + 1, last + 1)
            elif last in omit:
                term_range = range(0, omit[0])

        wn_score = 0.0
        syn_score = 0.0
        #todo: take some combination of the two scores
        for i in term_range:
            term = self.terms[i]
            wn_score += common.compare_related_words(term.related_words,
                                                  soln_words)
            syn_score += common.compare_syns(term.syns, soln_syns)

        logging.info("wn_score: " + str(wn_score))
        logging.info("syn_score: " + str(syn_score))
        return syn_score / len(term_range)
