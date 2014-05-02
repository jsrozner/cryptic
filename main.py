import argparse
import logging
import re

from anagrammer import Anagrammer
from clue import Clue
from lib import mystring
from solvers.anagramsolver import AnagramSolver
from solvers.doublesolver import DoubleSolver
from solvers.hiddensolver import HiddenSolver
from solvers.reversesolver import ReverseSolver


# corpuses
anagram_indicator_file = "data/anagram.txt"
hidden_indicator_file = "data/hidden.txt"
reverse_indicator_file = "data/reversal.txt"

# other data files
anagram_database_file = "data/anagrams.db"

# allow args to be accessed in other files
cmd_line_args = None


class Parser(object):
    """ A parser.

    Attributes:
        solvers
        aux_solvers
    """
    def __init__(self):
        # Generate solvers.
        anagrammer = Anagrammer(anagram_database_file)

        anagram_solver = AnagramSolver(anagram_indicator_file, anagrammer)
        double_solver = DoubleSolver()
        hidden_solver = HiddenSolver(hidden_indicator_file, anagrammer)
        reverse_solver = ReverseSolver(reverse_indicator_file, anagrammer)

        self.solvers = [anagram_solver, hidden_solver, reverse_solver]
        self.aux_solvers = [double_solver]

    def parse(self, input_line, print_solns=True):
        """ Parse a given line of input.

        :param str input_line:
        :param bool print_solns: Whether to print solns
        :return: List of solution objects
        :rtype: list[solution.Solution]
        """

        # expect "... (len)"
        # todo: implement double clues
        if re.search("\(\d,\d\)$", input_line):
            logging.warning("Double clues aren't implemented yet.")
            return []

        # allow lengths given outside of parenthesis
        split = re.search("(.*)(\d|\(\d\))$", input_line)
        if not split:
            logging.warning("No length specified")
            return []

        clue_words = split.group(1).strip()
        answer_length = split.group(2)
        try:
            answer_length = int(mystring.strip_punctuation(answer_length))
        except ValueError:
            logging.warning("No answer length given for clue")
            return []

        clue = Clue(clue_words, answer_length)

        solns = []
        for s in self.solvers:
            logging.info("Running " + str(s))
            new_solns = s.get_solutions(clue)
            logging.info(str(s) + " got " + str(len(new_solns)) + " solutions")
            solns += new_solns
        solns = sorted(solns)

        # run secondary, expensive solvers
        # todo: this is an arbitrary cutoff
        if not solns or solns[-1].score < 100.0:
            logging.info("Running auxiliary solvers")
            for s in self.aux_solvers:
                logging.info("Running " + str(s))
                new_solns = s.get_solutions(clue)
                logging.info(str(s) + " got " + str(len(new_solns)) + " solns")
                solns += new_solns
        solns = sorted(solns)

        # todo: get rid of duplicates?
        # todo: scale relative anagramers
        ret = sorted(solns)[-cmd_line_args.num_solns:]
        if print_solns:
            for soln in ret:
                if cmd_line_args.no_solution_breakdown:
                    print soln.solution
                else:
                    print str(soln) + "\n"

        return ret


def main():
    # Parse commandline arguments
    arg_parser = argparse.ArgumentParser(description='Cryptic crossword solver.')
    arg_parser.add_argument("-v", "--logging", type=str, default="DEBUG",
                            help='Verbosity logging ')
    arg_parser.add_argument("--no-solution-breakdown", action="store_true",
                            help="Print only solution words with no "
                                 "explanation.")
    arg_parser.add_argument("--num-solns", type=int, default=10,
                            help="Number of solutions to show.")
    arg_parser.add_argument("--input-file", type=str, default="",
                            help="Run on input list of clues, not interactive")
    arg_parser.add_argument("--use-wn", action="store_true",
                            help="Use wordnet rather than thesaurus")
    arg_parser.add_argument("--test", type=str, default="",
                            help="Run test file")
    global cmd_line_args
    cmd_line_args = arg_parser.parse_args()

    # Set logging level
    logging_level = getattr(logging, cmd_line_args.logging.upper())
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % cmd_line_args.logging)
    logging.basicConfig(level=logging_level)
    logging.info("Setting verbosity to " + str(cmd_line_args.logging))

    parser = Parser()

    test_print = True
    if cmd_line_args.test != "":
        print "Running in test mode..."
        correct = 0
        correct_but_not_first = 0
        total = 0
        with open(cmd_line_args.test, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                total += 1
                clue = lines[i]
                correct_soln = lines[i + 1].strip()

                if test_print:
                    print "--------------"
                    print clue
                    print "expect soln: " + correct_soln

                solns = parser.parse(clue, print_solns=test_print)
                if solns and solns[0].solution == correct_soln:
                    correct += 1
                else:
                    for s in solns[1:]:
                        if s.solution == correct_soln:
                            correct_but_not_first += 1
        print "Out of total: %d\t %d correct\t %d correct but not first" % \
              (total, correct, correct_but_not_first)

    elif cmd_line_args.input_file == "":
        print "Running in interactive mode...\n" \
              "Clues should be of the form '....(num)'"
        while True:
            line = raw_input()
            parser.parse(line)
    else:
        print "Running in file input mode..."
        with open(cmd_line_args.input_file, "r") as f:
            for line in f.readlines():
                print line
                parser.parse(line)


main()
