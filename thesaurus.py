import logging
import shelve

thesaurus_database_file = "data/thesaurus.db"
thesaurus_back_database_file = "data/thesaurus_aux.db"

class Thesaurus(object):
    def __init__(self, thesaurus_database, thesaurus_database_back):
        try:
            self.thes = shelve.open(thesaurus_database, "r")
            self.back_thes = shelve.open(thesaurus_database_back, "r")
        except:
            logging.exception("Failed to open a thesaurus")
            self.thes = None
            self.back_thes = None

    def thes_look_up(self, word):
        if word in self.thes:
            return self.thes[word]
        else:
            return []

    def back_look_up(self, word):
        all_syns = []
        if word in self.back_thes:
            syns = self.back_thes[word]
            for s in syns:
                all_syns += self.thes_look_up(s)

        return all_syns

    def internal_get_synonyms(self, word):
        return sorted(set(self.thes_look_up(word) + self.back_look_up(word)))
    
    def get_synonyms(self, word, depth=1):
        word = word.lower()     # this is probably unnecessary

        syns = []
        all_syns = set(word)
        syns.append(all_syns) # all_syns[0] = word
        
        for i in range(1, depth):
            new_syns = []
            for syn in syns[i - 1]:
                new_syns += self.internal_get_synonyms(word)

            new_syns = set(new_syns).difference(all_syns)    # don't repeat syns
            syns.append(new_syns)       # syns[i]
            all_syns = all_syns.union(new_syns)

        return syns


thesaurus = Thesaurus(thesaurus_database_file, thesaurus_back_database_file)
