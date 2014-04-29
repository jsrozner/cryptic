import shelve
from bisect import insort

db = shelve.open("anag", "n")

with open("/usr/share/dict/web2") as f:
    for x in f.readlines():
        x = x.strip()
        str = "".join(sorted(x))
        if str in db:
            temp = db[str]
            insort(temp, x)
            db[str] = temp
        else:
            db[str] = [x]

db.close()
