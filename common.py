from bisect import bisect_left
from difflib import get_close_matches
from os.path import isfile
from nltk.corpus import wordnet as wn

import mystring

kMinSynWordLength = 4

def getRelatedWords(word, should_include_def_terms=False, depth=2):
  allsyns = [word]
  for synset in wn.synsets(word):
    for lemma_name in synset.lemma_names:
      allsyns.append(lemma_name)
    for hypernym in synset.hypernyms():
      for lemma_name in hypernym.lemma_names:
        allsyns.append(lemma_name)
    for hyponym in synset.hyponyms():
      for lemma_name in hyponym.lemma_names:
        allsyns.append(lemma_name)

    if should_include_def_terms:
      for def_term in synset.definition.split():
        stripped_term = mystring.stripPunctuation(def_term)
        if len(word) >= kMinSynWordLength:
          allsyns.append(word)

  if depth > 1:
    final = []
    for word in sorted(set(allsyns)):
      final += getRelatedWords(word, should_include_def_terms, depth - 1)

    return sorted(set(final))

  return sorted(set(allsyns))

  return sorted(set(allsyns))


class IndicatorDictionary:
  kMinIndicatorDistance = 0.65
  def __init__(self, indicator_file):
    if isinstance(indicator_file, basestring):
      print "opened indicator file"
      with open(indicator_file) as f:
        self.dict = [x.strip() for x in f.readlines()]
    else:
      self.dict = indicator_file

  def lookup(self, word):
    i = bisect_left(self.dict, word)
    match = get_close_matches(word, self.dict[i-1:i+1], n=1,
                              cutoff=self.kMinIndicatorDistance)
    if match:
      return match[0]
    else:
      return None






