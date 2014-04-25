import enchant

from itertools import permutations
from solver import IndicatorSolver


class AnagramSolver(IndicatorSolver):
  def __init__(self, indicator_file):
    print "initializing anagram solver"
    IndicatorSolver.__init__(self, indicator_file)
    self.dict = enchant.Dict("en_US")

  def getAnagramSolutions(self, clue):
    print "getting anagram solutions"
    possible_solutions = []
    for term in clue.terms:
      print "looking up term ", term.word
      if self.indicators.lookup(term.word) is not None:
        print "got indicator"
        (single_word_indices, double_word_indices) = self.getValidLengthCombos(
          clue.word_lengths, clue.answer_length)

        #todo: handle double words
        for pos in single_word_indices:
          word_to_permute = clue.terms[pos].word
          anagrams = self.getValidPermutations(word_to_permute)
          for a in anagrams:
            print "valid anagram ", a
            if clue.checkDefinition(a):
              possible_solutions.append(a) #todo make explanation note

    return possible_solutions

  def getValidPermutations(self, word):
    valid_perms = []
    for p in permutations(word):
      w = "".join(p)
      if self.dict.check(w):
        valid_perms.add(w)

    return valid_perms

  # todo: this function should pop out things like "with"
  # todo: handles only two word combos
  def getValidLengthCombos(word_lengths, goal_length):
    single_word_indices = []
    double_word_indices = []

    # Look over pairs of words only
    for i in range(0, len(word_lengths) - 1):
      if(word_lengths[i] == goal_length):
        single_word_indices.append(i)
      elif(word_lengths[i] + word_lengths[i+1] == goal_length):
        double_word_indices.append(i)

    return (single_word_indices, double_word_indices)
