# Josh Rozner

import argparse

from anagramsolver import AnagramSolver

# corpuses
anagram_indicator_file = "data/anagram.txt"
anagram_database_file = "data/anagrams.db"

class Solution:
    """ Encapsulates cryptic crossword solutions

    Attributes:
        score: an indication of how likely the solution is to be correct
        notes: newline separated notes on the derivation of the solution
        solution: the word believed to be a solution
    """
    def __init__(self):
        self.score = -1
        self.notes = []
        self.solution = ""

    def addNote(self, note):
        """ Add a note to a solution

        :param note: string : the note to be added
        """
        self.notes.append(note)

    @property
    def __str__(self):
        ret = "Solution: %s\t Score: %d\t\n", self.solution, self.score
        ret += "\n".join(self.notes)
        return ret


def main():
    # Parse commandline arguments
    parser = argparse.ArgumentParser(description='Cryptic crossword solver.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()

    # Generate solvers. todo: consider a configuration file
    anagram_solver = AnagramSolver(anagram_indicator_file,
                                   anagram_database_file)
    while True:
        line = raw_input()
        clue = clue.Clue(line)
        solns = anagram_solver.getAnagramSolutions(clue)
        print "possible solutions:"
        for soln in sorted(set(solns)):
            print soln


main()
