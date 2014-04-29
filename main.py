import argparse
import logging

from anagrammer import Anagrammer
from anagramsolver import AnagramSolver
from clue import Clue

# corpuses
anagram_indicator_file = "data/anagram.txt"
anagram_database_file = "data/anagrams.db"




def main():
    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='Cryptic crossword solver.')
    parser.add_argument("-l", "--logging", type=str, default="INFO",
                        help='Verbosity logging ')

    args = parser.parse_args()

    logging_level = getattr(logging, args.logging.upper())
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % args.logging)
    logging.basicConfig(level=logging_level)
    logging.info("Setting verbosity to " + str(args.logging))

    # Generate solvers. todo: consider a configuration file
    anagrammer = Anagrammer(anagram_database_file)
    anagram_solver = AnagramSolver(anagram_indicator_file, anagrammer)

    while True:
        line = raw_input()
        clue = Clue(line)
        solns = anagram_solver.get_anagram_solutions(clue)
        print "possible solutions:"
        # todo: get rid of duplicates
        for soln in solns:
            print str(soln) + "\n"


main()
