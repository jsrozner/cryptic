import mystring
import common
'''
isuppercase: whether term was initially uppercased
word: the actual lowercased word
defStrings: an array of words found in wordnet definitions
'''


class Term:
    def __init__(self, input):
        if mystring.startsWithUpperCase(input):
            self.isUpperCase = True
        else:
            self.isUpperCase = False

        self.word = input.lower()

        related_words = common.getRelatedWords(self.word, True, 2)
        print related_words
        self.allDefinitions = IndicatorDictionary(sorted(set(related_words)))


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
        clue = mystring.stripPunctuation(clue)  # remove punctuation
        clueWords = clue.split()

        try:
            self.answer_length = int(clueWords[-1])
        except:
            print("No length of clue given.")
            return

        clueWords = clueWords[0:-1]  # strip out length
        self.word_lengths = map(len, clueWords)
        self.terms = map(Term, clueWords)

    def checkDefinition(self, possible_solution):
        related_words = common.getRelatedWords(possible_solution, True, 2)
        print related_words
        for term in self.terms:
            if term.allDefinitions.lookup(possible_solution) is not None:
                return True

        for word in related_words:
            if term.allDefinitions.lookup(word) is not None:
                return True

        return False