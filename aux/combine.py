with open("data/anagram.txt") as f1:
    with open("data/anagram2.txt") as f2:
        set1 = set([x.strip() for x in f1.readlines()])
        set2 = set([x.strip() for x in f2.readlines()])

        union = sorted(set1.union(set2))

        with open("data/anagram3.txt", "w") as f3:
            for w in union:
                f3.write(w + "\n")

