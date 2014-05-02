import logging
import shelve


class Anagrammer(object):
    """ Anagram database

    Attributes:
        db: opened anagram database
    """
    def __init__(self, anagram_database):
        try:
            self.db = shelve.open(anagram_database, "r")
        except IOError:
            logging.exception("Failed to open anagram database")
            self.db = None

        logging.debug("Opened anagram database successfully")

    def __look_up(self, word):
        """ Perform a lookup on a set of characters. Internal method.

        :param str word: letters to use in lookup
        :return: Valid anagrams
        :rtype: list[str]
        """
        lookup = "".join(sorted(word))  # Sort for hashing, essentially
        if lookup in self.db:
            return self.db[lookup]
        else:
            return []

    def get_anagrams(self, letters):
        """ Return valid anagrams of letters. Don't include the strint that
            was passed in.

        :param str letters: Letters to be anagrammed
        :return: List of valid anagrams
        :rtype: list[str]
        """
        logging.debug("Looking up in anagram db: " + letters)
        results = self.__look_up(letters)

        # don't return the letters themselves
        if letters in results:
            results.remove(letters)
        return results

    def is_word(self, word):
        """ Check if word is present in our anagram dictionary

        :param str word:
        :return: True if present in anagram dictionary
        :rtype: bool
        """
        results = self.__look_up(word)
        return word in results
