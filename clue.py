import logging

from lib import common, mystring
from thesaurus import thesaurus


# How deep to search in wordnet and thesaurus
related_word_depth = 2


class Term:
    """ Component of a clue.
    
    Attributes:
        is_upper_case: whether term initially started with upper case letter
        word: actual lower-cased word
        related_words: tuple of (syns, defs). syns and defs are both arrays
    """
    def __init__(self, word):
        """
        :param str word: The initial word of the clue
        """
        self.is_upper_case = mystring.starts_with_upper_case(word)
        self.word = word.lower()

        depth = related_word_depth
        logging.debug("Getting words related to " + self.word + " with depth " +
                      str(depth))
        self.related_words = common.get_wn_related_words(self.word, depth)
        self.syns = thesaurus.get_all_synonyms(self.word, depth)
        self.small_syn_set = thesaurus.get_small_syn_set(self.word)
        logging.debug(self.syns)


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
    def __init__(self, clue, answer_length):
        """
        :param str clue: input line
        :param int answer_length: input length
        """
        self.original_clue = clue
        self.answer_length = answer_length

        self.ends_with_question = clue[-1] == "?"
        self.ends_with_exclamation = clue[-1] == "!"
        logging.debug("Clue ends with question: " +
                      str(self.ends_with_question))
        logging.debug("Clue ends with exclamation: " +
                      str(self.ends_with_exclamation))

        input_clue = mystring.strip_punctuation(clue)  # remove punctuation
        self.clue_words = input_clue.split()

        self.word_lengths = map(len, self.clue_words)
        self.terms = map(Term, self.clue_words)

    def check_definition(self, soln, omit=None, split_in_half=True):
        """ Get a score for similarity

        :param str soln: the tentative solution
        :param list[int] omit: indices of words in the clue to omit
        :param bool split_in_half: whether to search only one side for defn
        :return: score
        :rtype: float
        """
        logging.debug("Checking definition for soln: " + soln)

        if omit is None:
            omit = []

        depth = related_word_depth
        soln_words = common.get_wn_related_words(soln, depth)
        soln_syns = thesaurus.get_all_synonyms(soln, depth)

        last = len(self.terms) - 1  # index of last term
        omit = sorted(set(omit))    # don't allow repeated values

        term_range = range(0, last)  # default term range

        # Take only one half of the clue if split_in_half is true
        if omit and split_in_half:
            if 0 in omit and last in omit:  # both sides of clue are used
                logging.debug("Both sides of clue are used. Score is 0.0")
                return 0.0
            elif 0 in omit:
                term_range = range(omit[-1] + 1, last + 1)
            elif last in omit:
                term_range = range(0, omit[0])

        #todo: take some combination of the two scores
        wn_score = 0.0
        syn_score = 0.0
        for i in term_range:
            term = self.terms[i]
            wn_score += common.compare_wn_related_words(term.related_words,
                                                        soln_words)
            syn_score += common.compare_syns(term.syns, soln_syns)

        logging.info("wn_score: " + str(wn_score))
        logging.info("syn_score: " + str(syn_score))
        if wn_score > syn_score:
            return wn_score / len(term_range)
        else:
            return syn_score / len(term_range)
