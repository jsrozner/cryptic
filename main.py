import argparse
import logging

from anagrammer import Anagrammer
from clue import Clue
from solvers.anagramsolver import AnagramSolver
from solvers.doublesolver import DoubleSolver
from solvers.hiddensolver import HiddenSolver
from thesaurus import Thesaurus


# corpuses
anagram_indicator_file = "data/anagram.txt"
hidden_indicator_file = "data/hidden.txt"

anagram_database_file = "data/anagrams.db"


def main():
    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='Cryptic crossword solver.')
    parser.add_argument("-v", "--logging", type=str, default="INFO",
                        help='Verbosity logging ')
    parser.add_argument("--no-solution-breakdown",
                        help="Print only solution words with no explanation.")
    parser.add_argument("--num-solns", type=int, default=10,
                        help="Number of solutions to show.")

    args = parser.parse_args()

    logging_level = getattr(logging, args.logging.upper())
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % args.logging)
    logging.basicConfig(level=logging_level)
    logging.info("Setting verbosity to " + str(args.logging))

    # Generate solvers. todo: consider a configuration file
    anagrammer = Anagrammer(anagram_database_file)

    anagram_solver = AnagramSolver(anagram_indicator_file, anagrammer)
    double_solver = DoubleSolver()
    hidden_solver = HiddenSolver(hidden_indicator_file, anagrammer)

    solvers = [anagram_solver, hidden_solver]
    aux_solvers = [double_solver]

    while True:
        line = raw_input()
        clue = Clue(line)
        solns = []

        for s in solvers:
            solns += s.get_solutions(clue)
        solns = sorted(solns)
        # todo: arbitrary cutoff
        if not solns or solns[-1].score < 100.0:       # run secondary, expensive solvers
            for s in aux_solvers:
                solns += s.get_solutions(clue)
        print "possible solutions:"
        # todo: get rid of duplicates?
        # scale relative anagramers
        for soln in sorted(solns)[-args.num_solns:]:
            if args.no_solution_breakdown:
                print soln.solution + "\n"
            else:
                print str(soln) + "\n"


main()
