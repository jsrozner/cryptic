import shelve
import sys

testword = ""
try:
    testword = sys.argv[1]
except:
    print "no arg given"
    exit

db = shelve.open("data/anagrams.db", "r")

lookup = "".join(sorted(testword.strip()))
print lookup
if lookup in db:
    print db[lookup]
else:
    print testword + " not found"

db.close()