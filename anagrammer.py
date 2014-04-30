import logging
import shelve


class Anagrammer(object):
    def __init__(self, anagram_database):
        try:
            self.db = shelve.open(anagram_database, "r")
        except:
            logging.exception("Failed to open anagram database")
            self.db = None

    def look_up(self, word):
        lookup = "".join(sorted(word))
        if lookup in self.db:
            return self.db[lookup]
        else:
            return []


    def get_anagrams(self, letters):
        results = self.look_up(letters)

        # don't return the letters themselves
        if letters in results:
            results.remove(letters)
        return results

    def isWord(self, word):
        results = self.look_up(word)
        if word in results:
            return True

        return False

