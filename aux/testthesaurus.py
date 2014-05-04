"""
Get the synonyms and back-synonyms associated with a given word.

Usage: python tesththesaurus.py <lookup-word>
"""


import shelve
import sys

testword = ""
try:
    testword = sys.argv[1]
except:
    print "no arg given"
    exit

print "looking up in main thesaurus"
db = shelve.open("data/thesaurus.db", "r")
lookup = testword.strip()

if lookup in db:
    print db[lookup]
else:
    print lookup + " not found"

db.close()

print "looking up in aux thesaurus"
db = shelve.open("data/thesaurus_aux.db")
lookup = testword.strip()

if lookup in db:
    print db[lookup]
else:
    print lookup + " not found"

db.close()
