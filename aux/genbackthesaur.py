"""
Generate a back-mapped thesaurus from an input thesaurus file.

For a word w that maps to a set S of synonyms,
For every y in S, add an entry that maps y to w.
"""


import shelve

db = shelve.open("data/thesaurus_aux.db")

with open("mthesaur.txt") as f:
    for x in f.readlines():
        x = x.strip().lower()
        all_words = x.split(",")  # omit first word
        first = all_words[0]
        rest = all_words[1:]
        for word in rest:
            if " " in word:  # omit spaced words
                continue
            temp = []
            if word in db:
                temp = db[word]  #todo: sort these

            temp.append(first)
            db[word] = temp

db.close()
