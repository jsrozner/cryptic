"""
Generate a thesaurus from a thesaurus text file.

"""


import shelve

db = shelve.open("data/thesaurus.db")

with open("/Users/Downloads/mthes10/mthesaur.txt") as f:
    for x in f.readlines():
        x = x.strip().lower()
        all_words = x.split(",")
        word = all_words[0]
        syns = all_words[1:]
        db[word] = syns

db.close()
