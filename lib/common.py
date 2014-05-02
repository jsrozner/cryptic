from nltk.corpus import wordnet as wn

# Required min length to be used in a definition.
# todo: This should be implemented using "stop sets"
min_def_word_length = 4

# todo: wn-tuples should be represented as a class
# todo: add more debugging for syn / def comparisons


def get_wn_synonyms(words):
    """ Return synonyms, hypernyms, and hyponyms for all words in words

    :param list[str] words: The words for which to find synonyms
    :return set[str]: Set of all syns, hypernyms, and hyponyms. (No duplicates)
    """
    syns = []
    for w in words:
        for synset in wn.synsets(w):
            for lemma_name in synset.lemma_names:
                syns.append(lemma_name)
            for hypernym in synset.hypernyms():
                for lemma_name in hypernym.lemma_names:
                    syns.append(lemma_name)
            for hyponym in synset.hyponyms():
                for lemma_name in hyponym.lemma_names:
                    syns.append(lemma_name)
    return set(syns)


def get_wn_definition(words):
    """ For all words in words, get the definitions associated with all synsets.
        Throw away words in the definitions shorter than min_def_word_length.

    :param list[str] words: The words for which to get definitions
    :return set[str]: Set of all definition words >= min length
    """
    defs = []
    for w in words:
        for synset in wn.synsets(w):
            for def_term in synset.definition.split():
                if len(def_term) >= min_def_word_length:
                    defs.append(def_term)
    return set(defs)


def get_wn_related_words(word, depth=2):
    """ Get syns and defs for word up to search depth, depth (how many
        iterations of searches to perform before stopping)

    :param str word: The word for which to get syns
    :param int depth: How many iterations to search
    :return (list[set[str]], list[set[str]]): Tuple of syns and defs, the
        indices give the depth
    """

    syns = []
    defs = []

    # Keep track of syns and defs we've already seen (don't repeat)
    allsyns = set(word)
    syns.append(allsyns)  # syns[0] syns only of input word

    first_defs = get_wn_definition([word])
    alldefs = set(first_defs)
    defs.append(alldefs)  # defs[0] def only of input word

    # Iterate over depth
    for i in range(1, depth):
        new_syns = set(get_wn_synonyms(syns[i - 1]))  # syns of prev level
        new_syns = new_syns.difference(allsyns)       # take only new ones
        syns.append(new_syns)                         # syns[i]
        allsyns = allsyns.union(new_syns)             # update all syns

        # For defs, take defs of syns[i - 1] and defs of defs[i - 1]
        new_defs = set(get_wn_definition(syns[i - 1].union(defs[i - 1])))
        new_defs = new_defs.difference(alldefs)  # take only new defs
        defs.append(new_defs)                    # defs[i]
        alldefs = alldefs.union(new_defs)

    return syns, defs


def compare_wn_related_words(tup1, tup2):
    """ Compare two tuples by effectively taking a weighted cross product

    :param (list[set[str]], list[set[str]]) tup1: First tuple to compare
    :param (list[set[str]], list[set[str]]) tup2: Second tuple to compare
    :return float: The cumulative score
    """
    syns1 = tup1[0]
    defs1 = tup1[1]
    syns2 = tup2[0]
    defs2 = tup2[1]

    score = 0.0
    for i in range(0, len(syns1)):  # syns and defs should be same length
        for j in range(0, len(syns2)):
            # get the various intersections
            same_syns = syns1[i].intersection(syns2[j])
            same_defs = defs1[i].intersection(defs2[j])

            # cleverly compute def and syn cross
            all_syns = syns1[i].union(syns2[j])
            all_defs = defs1[i].union(defs2[j])
            syn_defs = all_syns.intersection(all_defs)

            # weight according to depth and syn vs definition.
            # syn is weighted exponentially over definition
            score += 1.0 / (1 + (i * j)) * len(same_syns)
            score += 1.0 / (2 << (i + j + 1)) * len(same_defs)
            first_mux = max(i, j) + 1
            second_mux = max(min(i, j), 1)
            score += 1.0 / ((2 << first_mux) * second_mux) * len(syn_defs)

    return score


def get_syn_intersection(syns1, syns2):
    """ Get intersection of two thesaurus sets

    :param set[str] syns1:
    :param set[str] syns2:
    :return set[str]: The intersection of the two syn sets
    """
    return syns1.intersection(syns2)


def compare_syns(syns1, syns2):
    """ Score the similarity of two syn sets. Weight based on depth of syns.

    :param set[str] syns1:
    :param set[str] syns2:
    :return: Weighted (by depth) score of intersection
    """
    score = 0.0
    for i in range(0, len(syns1)):
        for j in range(0, len(syns2)):
            same_syns = syns1[i].intersection(syns2[j])
            score += 1.0 / (1 + (i * j)) * len(same_syns)

    return score
