"""
Augment an anagrams database with words from a new dictionary.
"""


import shelve
import bisect

db = shelve.open("data/anagrams.db")

with open("US.dic") as f:
    for x in f.readlines():
        x = x.strip()
        str = "".join(sorted(x))
        if str in db:
            temp = db[str]
            pos_left = bisect.bisect_left(temp, x)
            pos_right = bisect.bisect_right(temp, x)
            if pos_left == pos_right:
                bisect.insort(temp, x)
                db[str] = temp
        else:
            db[str] = [x]

db.close()
