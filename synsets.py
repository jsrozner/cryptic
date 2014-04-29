from nltk.corpus import wordnet as wn


def printsyns(s):
    for syn in wn.synsets(s):
        for l in syn.lemmas:
            print l
            print l.name
        print syn.definition
