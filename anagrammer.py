import logging
import shelve


class Anagrammer(object):
    def __init__(self, anagram_database):
        try:
            self.db = shelve.open(anagram_database, "r")
        except:
            logging.exception("Failed to open anagram database")
            self.db = None

    def getAnagrams(self, lookup):
        if lookup in self.db:
            return db[lookup]
        else:
            return []



