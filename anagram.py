import enchant

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

def getPossibleWordsToAnagram():
  return getValidLengthCombos()

def handleAnagram(indicator_pos, word_set):
  possible_solutions = []

  (single_word_indices, double_word_indices) = getValidLengthCombos(
    word_lengths, goal_length)

  for pos in single_word_indices:
    word_to_permute = word_set[pos]
    anagrams = getAllPermutations(word_to_permute)
    for a in anagrams:
      if isWord(a) and checkDefinition(pos, a, word_set):
        possible_solutions.append(a) #todo make explanation note
