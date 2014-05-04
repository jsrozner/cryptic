"""
Take a list of new-line separated clues and prompt the user for the answer.
Print a new file that is of the form below, for use with main.py --test.

clue
soln
clue
soln
"""


import sys

with open(sys.argv[1], "r") as f:
    out = open(sys.argv[1] + ".test", "w")

    for line in f.readlines():
        print line
        out.write(line)
        soln = raw_input()
        out.write(soln + "\n")
