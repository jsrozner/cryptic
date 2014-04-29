import common
import mystring
import logging
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
        related_words = common.getRelatedWords(self.word, True, depth)
        logging.debug("Words related to " + self.word + " with depth " +
                      str(depth) + str(related_words))
        self.allDefinitions = \
            common.IndicatorDictionary(sorted(set(related_words)))


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

    def check_definition(self, possible_solution):
        related_words = common.getRelatedWords(possible_solution, True, 2)
        for term in self.terms:
            if term.allDefinitions.lookup(possible_solution) is not None:
                return 1.0

        for word in related_words:
            if term.allDefinitions.lookup(word) is not None:
                return 0.5

        return -1.0