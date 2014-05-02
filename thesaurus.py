import logging
import shelve

thesaurus_database_file = "data/thesaurus.db"
thesaurus_back_database_file = "data/thesaurus_aux.db"


class Thesaurus(object):
    """ Class that holds a thesaurus database

    Attributes:
        thes: normal forward word->list of syns mapping
        back_thes: mapping from word -> list of words that contain this word
            as a synonym
    """

    def __init__(self, thesaurus_database, thesaurus_database_back):
        try:
            self.thes = shelve.open(thesaurus_database, "r")
            self.back_thes = shelve.open(thesaurus_database_back, "r")
        except IOError:
            logging.exception("Failed to open a thesaurus")
            self.thes = None
            self.back_thes = None

    def thes_look_up(self, word):
        """ Get forward synonyms for word

        :param str word: The lookup word
        :return: List of forward synonyms
        :rtype: list[str]
        """
        if word in self.thes:
            return self.thes[word]
        else:
            return []

    def back_look_up(self, word):
        """ Get syns of all words that have this word in their syn sets

        :param str word:
        :return: list of syns after getting back_syns
        :rtype: list[str]
        """
        all_syns = []
        if word in self.back_thes:
            syns = self.back_thes[word]
            for s in syns:
                all_syns += self.thes_look_up(s)

        return all_syns

    def __internal_get_all_synonyms(self, word):
        """
        :param str word:
        :return: Sorted list of all syns
        :rtype: list[str]
        """
        return sorted(set(self.thes_look_up(word) + self.back_look_up(word)))

    def get_all_synonyms(self, word, depth=1):
        """ Get all syns of a word up to depth

        :param str word:
        :param int depth:
        :return: list of syns
        :rtype: list[str]
        """
        word = word.lower()  # this is probably unnecessary

        syns = []
        all_syns = set(word)
        syns.append(all_syns)  # all_syns[0] = word

        for i in range(1, depth):
            new_syns = []
            for syn in syns[i - 1]:
                new_syns += self.__internal_get_all_synonyms(syn)

            new_syns = set(new_syns).difference(all_syns)  # don't repeat syns
            syns.append(new_syns)  # syns[i]
            all_syns = all_syns.union(new_syns)

        return syns


thesaurus = Thesaurus(thesaurus_database_file, thesaurus_back_database_file)
