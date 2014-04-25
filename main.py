# Josh Rozner

import anagram
import mystring

from anagram import AnagramSolver
from common import IndicatorDictionary

from nltk.corpus import wordnet as wn

'''settings'''
kMinDefinitionWordLength = 4

'''corpuses'''
kAnagramIndicatorFile = "anagram.txt"

'''
solution word
score
notes
'''
class Solution:
  def __init__(self):
    self.score = -1
    self.notes = []
    self.solution = ""

  def addNote(self, note):
    self.notes.append(note)

  def __str__(self):
    ret = "Solution: %s\t Score: %d\t\n", self.solution, self.score
    ret += "\n".join(self.notes)


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

    allDefinitions = []
    for synset in wn.synsets(self.word):
      for word in synset.definition.split():
        if len(word) >= kMinDefinitionWordLength:
          allDefinitions.append(synset.definition)
    self.allDefinitions = IndicatorDictionary(allDefinitions.sort())

''' original clue
answerlength
terms
'''
class Clue:
  # flags
  endsWithQuestion = False
  endsWithExclamation = False # todo: this and question mark not handled
  hasCapitals = False   # todo: never changed
  #todo: length

  def __init__(self, clue):
    self.originalClue = clue
    # todo: consider removing punctuation post separation
    clue = mystring.stripPunctuation(clue) # remove punctuation
    clueWords = clue.split()

    try:
      self.answer_length = int(clueWords[-1])
    except:
      print("No length of clue given.")
      return

    clueWords = clueWords[0:-1] # strip out length
    print clueWords
    self.word_lengths = map(len, clueWords)
    print self.word_lengths
    self.terms = map(Term, clueWords)
    print self.word_lengths

  def checkDefinitions(self, possible_solution):
    for term in self.terms:
      if term.allDefinitions.lookup(possible_solution) is not None:
        return 1

def main():
  anagram_solver = AnagramSolver(kAnagramIndicatorFile)
  while True:
    line = raw_input()
    clue = Clue(line)
    solns = anagram_solver.getAnagramSolutions(clue)
    for soln in solns:
      print soln

main()
