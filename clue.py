import logging

from lib import common, mystring

#todo: fix commenting in this file
'''
isuppercase: whether term was initially uppercased
word: the actual lowercased word
defStrings: an array of words found in wordnet definitions
'''


class Term:
    def __init__(self, input):
        if mystring.starts_with_upper_case(input):
            self.isUpperCase = True
        else:
            self.isUpperCase = False

        self.word = input.lower()

        depth = 2
        self.related_words = common.get_related_words(self.word, depth)
        logging.debug("Words related to " + self.word + " with depth " +
                      str(depth))


''' original clue
answerlength
terms
'''


class Clue:
    # flags
    endsWithQuestion = False
    endsWithExclamation = False  # todo: this and question mark not handled
    hasCapitals = False  # todo: never changed
    # todo: length

    def __init__(self, clue):
        self.originalClue = clue
        # todo: consider removing punctuation post separation
        clue = mystring.strip_punctuation(clue)  # remove punctuation
        clueWords = clue.split()

        try:
            self.answer_length = int(clueWords[-1])
        except:
            print("No length of clue given.")
            return

        clueWords = clueWords[0:-1]  # strip out length
        self.word_lengths = map(len, clueWords)
        self.terms = map(Term, clueWords)

    def check_definition(self, soln, omit=[], split_in_half=True):
        depth = 2
        soln_words = common.get_related_words(soln, depth)

        last = len(self.terms) - 1
        omit = sorted(set(omit))

        term_range = range(0, last) #default
        if omit and split_in_half:
            if 0 in omit and last in omit:
                return 0.0
            elif 0 in omit:
                term_range = range(omit[-1] + 1, last + 1)
            elif last in omit:
                term_range = range(0, omit[0])

        score = 0.0
        terms_counted = 0
        for i in term_range:
            terms_counted += 1
            term = self.terms[i]
            score += common.compare_related_words(term.related_words, soln_words)

        return score / terms_counted

