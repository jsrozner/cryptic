import logging

from bisect import bisect_left
from difflib import get_close_matches
from nltk.corpus import wordnet as wn


kMinDefWordLength = 4


def get_synonyms(words):
    syns = []
    for w in words:
        for synset in wn.synsets(w):
            for lemma_name in synset.lemma_names:
                syns.append(lemma_name)
            for hypernym in synset.hypernyms():
                for lemma_name in hypernym.lemma_names:
                    syns.append(lemma_name)
            for hyponym in synset.hyponyms():
                for lemma_name in hyponym.lemma_names:
                    syns.append(lemma_name)
    return set(syns)


def get_definition(words):
    defs = []
    for w in words:
        for synset in wn.synsets(w):
            for def_term in synset.definition.split():
                if len(def_term) >= kMinDefWordLength:
                    defs.append(def_term)
    return set(defs)


def get_related_words(word, depth=2):
    syns = []
    defs = []

    allsyns = set(word)
    syns.append(allsyns)  # syns[0]

    first_defs = get_definition([word])
    alldefs = set(first_defs)
    defs.append(alldefs)  # defs[0]

    for i in range(1, depth):
        new_syns = set(get_synonyms(syns[i - 1]))
        new_syns = new_syns.difference(allsyns)
        syns.append(new_syns)  # syns[i]
        allsyns = allsyns.union(new_syns)

        new_defs = set(get_definition(syns[i - 1].union(defs[i - 1])))
        new_defs = new_defs.difference(alldefs)
        defs.append(new_defs)  # defs[i]
        alldefs = alldefs.union(new_defs)

    return syns, defs


class IndicatorDictionary:
    kMinIndicatorDistance = 0.65

    #todo: this is ugly
    def __init__(self, indicator_file):
        if isinstance(indicator_file, basestring):
            with open(indicator_file) as f:
                self.dict = [x.strip() for x in f.readlines()]
            logging.info("Opened indicator file")
        else:
            self.dict = indicator_file

    def lookup(self, word):
        i = bisect_left(self.dict, word)
        match = get_close_matches(word, self.dict[i - 1:i + 1], n=1,
                                  cutoff=self.kMinIndicatorDistance)
        if match:
            return match[0]
        else:
            return None


def compare_related_words(tup1, tup2):
    syns1 = tup1[0]
    defs1 = tup1[1]
    syns2 = tup2[0]
    defs2 = tup2[1]

    score = 0.0
    for i in range(0, len(syns1)):
        for j in range(0, len(syns2)):
            same_syns = syns1[i].intersection(syns2[j])
            same_defs = defs1[i].intersection(defs2[j])
            all_syns = syns1[i].union(syns2[j])
            all_defs = defs1[i].union(defs2[j])
            syn_defs = all_syns.intersection(all_defs)

            score += 1.0 / (1 + (i * j)) * len(same_syns)
            score += 1.0 / (2 << (i + j + 1)) * len(same_defs)
            first_mux = max(i,j) + 1
            second_mux = max(min(i,j), 1)
            score += 1.0 / ((2 << first_mux) * second_mux) * len(syn_defs)

    return score

