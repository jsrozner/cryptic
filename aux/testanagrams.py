import shelve
import sys

testword = ""
try:
    testword = sys.argv[1]
except:
    print "no arg given"
    exit

db = shelve.open("anag", "r")

lookup = "".join(sorted(testword.strip()))
if lookup in db:
    print db[lookup]
else:
    print testword + " not found"

db.close()