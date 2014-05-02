import sys

with open(sys.argv[1], "r") as f:
    out = open(sys.argv[1] + ".test", "w")

    for line in f.readlines():
        print line
        out.write(line)
        soln = raw_input()
        out.write(soln + "\n")
