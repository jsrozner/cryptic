class Solution(object):
    """ Encapsulates cryptic crossword solutions

    Attributes:
        score: an indication of how likely the solution is to be correct
        notes: newline separated notes on the derivation of the solution
        solution: the word believed to be a solution
    """

    def __init__(self, soln, score, clue_type, indicator=""):
        """
        :type clue_type: solver.IndicatorType
        :type score: float
        :param clue_type:
        :param indicator: str
        :param soln: str
        :param score:
        """
        self.score = score
        note = 'Clue type ' + str(clue_type)
        if indicator:
            note += ' indicated by ' + indicator
        self.notes = [note]
        self.solution = soln

    def add_note(self, note):
        """ Add a note to a solution

        :param note: string : the note to be added
        """
        self.notes.append(note)

    def __str__(self):
        ret = "Solution: " + self.solution + "\t Score: " + str(self.score) + "\t\n"
        ret += "\n".join(self.notes)
        return ret

    def __cmp__(self, other):
        return cmp(self.score, other.score)
