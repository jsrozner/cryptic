import argparse
import logging

from anagrammer import Anagrammer
from clue import Clue
from solvers.anagramsolver import AnagramSolver
from solvers.doublesolver import DoubleSolver
from solvers.hiddensolver import HiddenSolver


# corpuses
anagram_indicator_file = "data/anagram.txt"
hidden_indicator_file = "data/hidden.txt"

anagram_database_file = "data/anagrams.db"


class Parser(object):
    def __init__(self, args):
        self.args = args
        # Generate solvers.
        anagrammer = Anagrammer(anagram_database_file)

        anagram_solver = AnagramSolver(anagram_indicator_file, anagrammer)
        double_solver = DoubleSolver()
        hidden_solver = HiddenSolver(hidden_indicator_file, anagrammer)

        self.solvers = [anagram_solver, hidden_solver]
        self.aux_solvers = [double_solver]

    def parse(self, input_line, print_solns=True):
        clue = Clue(input_line)
        solns = []

        for s in self.solvers:
            solns += s.get_solutions(clue)
        solns = sorted(solns)

        # todo: arbitrary cutoff
        # run secondary, expensive solvers
        if not solns or solns[-1].score < 100.0:
            for s in self.aux_solvers:
                solns += s.get_solutions(clue)

        # todo: get rid of duplicates?
        # todo: scale relative anagramers
        ret = sorted(solns)[-self.args.num_solns:]
        if print_solns:
            for soln in ret:
                if self.args.no_solution_breakdown:
                    print soln.solution
                else:
                    print "possible solutions:"
                    print str(soln) + "\n"

        return ret


def main():
    # Parse commandline arguments
    arg_parser = argparse.ArgumentParser(
        description='Cryptic crossword solver.')
    arg_parser.add_argument("-v", "--logging", type=str, default="DEBUG",
                            help='Verbosity logging ')
    arg_parser.add_argument("--no-solution-breakdown", action="store_true",
                            help="Print only solution words with no explanation.")
    arg_parser.add_argument("--num-solns", type=int, default=10,
                            help="Number of solutions to show.")
    arg_parser.add_argument("--input-file", type=str, default="",
                            help="Run on input list of clues, not interactive")
    arg_parser.add_argument("--use-wn", action="store_true",
                            help="Use wordnet rather than thesaurus")
    arg_parser.add_argument("--test", type=str, default="",
                            help="Run test file")
    args = arg_parser.parse_args()

    # Set logging level
    logging_level = getattr(logging, args.logging.upper())
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % args.logging)
    logging.basicConfig(level=logging_level)
    logging.info("Setting verbosity to " + str(args.logging))

    parser = Parser(args)

    if args.test != "":
        correct = 0
        correct_but_not_first = 0
        total = 0
        with open(args.test, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                total += 1
                clue = lines[i]
                correct_soln = lines[i + 1].strip()

                solns = parser.parse(clue, print_solns=False)
                if solns and solns[0].solution == correct_soln:
                    correct += 1
                else:
                    for s in solns[1:]:
                        if s.solution == correct_soln:
                            correct_but_not_first += 1
        print "Out of total: %d\t %d correct\t %d correct but not first" % \
              (total, correct, correct_but_not_first)

    elif args.input_file == "":
        while True:
            line = raw_input()
            parser.parse(line)
    else:
        with open(args.input_file, "r") as f:
            for line in f.readlines():
                print line
                parser.parse(line)


main()
