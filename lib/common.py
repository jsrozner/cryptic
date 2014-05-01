from nltk.corpus import wordnet as wn


min_def_word_length = 4


def get_wn_synonyms(words):
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
    defs = []
    for w in words:
        for synset in wn.synsets(w):
            for def_term in synset.definition.split():
                if len(def_term) >= min_def_word_length:
                    defs.append(def_term)
    return set(defs)


def get_related_words(word, depth=2):
    syns = []
    defs = []

    allsyns = set(word)
    syns.append(allsyns)  # syns[0]

    first_defs = get_wn_definition([word])
    alldefs = set(first_defs)
    defs.append(alldefs)  # defs[0]

    for i in range(1, depth):
        new_syns = set(get_wn_synonyms(syns[i - 1]))
        new_syns = new_syns.difference(allsyns)
        syns.append(new_syns)  # syns[i]
        allsyns = allsyns.union(new_syns)

        new_defs = set(get_wn_definition(syns[i - 1].union(defs[i - 1])))
        new_defs = new_defs.difference(alldefs)
        defs.append(new_defs)  # defs[i]
        alldefs = alldefs.union(new_defs)

    return syns, defs

def compare_related_words(tup1, tup2):
    syns1 = tup1[0]
    defs1 = tup1[1]
    syns2 = tup2[0]
    defs2 = tup2[1]

    score = 0.0
    for i in range(0, len(syns1)):  # syns and defs should be same length
        for j in range(0, len(syns2)):
            same_syns = syns1[i].intersection(syns2[j])
            same_defs = defs1[i].intersection(defs2[j])
            all_syns = syns1[i].union(syns2[j])
            all_defs = defs1[i].union(defs2[j])
            syn_defs = all_syns.intersection(all_defs)

            score += 1.0 / (1 + (i * j)) * len(same_syns)
            score += 1.0 / (2 << (i + j + 1)) * len(same_defs)
            first_mux = max(i,j) + 1
            second_mux = max(min(i,j), 1)
            score += 1.0 / ((2 << first_mux) * second_mux) * len(syn_defs)

    return score

def get_syn_intersection(syns1, syns2):
    '''d = dict()
    for i in range(0, len(syns1)):
        for j in range(0, len(syns2)):
            same_syns = syns1[i].intersection(syns2[j])
            key = i + j
            if key in d:
                temp = d[key]
                temp = temp.union(same_syns)
                d[key] = temp
            else:
                d[key] = same_syns

    '''
    return syns1.intersection(syns2)


def compare_syns(syns1, syns2):
    score = 0.0
    for i in range(0, len(syns1)):
        for j in range(0, len(syns2)):
            same_syns = syns1[i].intersection(syns2[j])
            score += 1.0 / (1 + (i * j)) * len(same_syns)

    return score


