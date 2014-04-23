# Josh Rozner

import enchant

import anagram
import mystring

class IndicatorType:
  Anagram = range(1)
  # should modify
  Left, Right = range(2)

class Indicator:
  ty = IndicatorType.Anagram

'''
isuppercase
'''
class Term:
  def __init__(self, input):
    if mystring.startsWithUpperCase(input):
      self.isUpperCase = True
    else:
      self.isUpperCase = False

    self.word = input.tolower()

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
      self.answerLength = int(clueWords[-1])
    except:
      print("No length of clue given.")
      return

    clueWords = clueWords[0:-1] # strip out length
    self.terms = map(Term(), clueWords)


def checkDefinition(possible_solution, )
  # get synsets
  # get definitions
  # check for contents


def getIndicators(term_set):
  for

def getSolutions(clue):
  solutions = []
  getIndicators


def parse(s):
  clue = Clue(s)

  #sort(getSolutions(clue))
  print("done")


def initialize():
  # read in indicator dictionaries


def main():
  initialize()
  while True:
    try:
      line = raw_input()
      print line
      parse(line)
    except:
      exit()

main()
