import logging
import shelve


class Anagrammer(object):
    def __init__(self, anagram_database):
        try:
            self.db = shelve.open(anagram_database, "r")
        except:
            logging.exception("Failed to open anagram database")
            self.db = None

    def getAnagrams(self, letters):
        lookup = "".join(sorted(letters))
        if lookup in self.db:
            temp = self.db[lookup]
            if letters in temp:
                temp.remove(letters)
            return temp
        else:
            return []
