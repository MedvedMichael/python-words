# The Fireman Problem
#
# Let's define a compound word to be a word that can be formed by concatenating
# two or more other words, each having a length greater than two. For instance,
# "fireman" is a compound word because it is the concatenation of "fire" and
# "man".
#
# Implement the following two functions to satisfy the test cases.
# Feel free to implement additional functions that you may need.
#
# This command runs the tests:
#
#     pytest -s fireman.py

import pytest
import string

def flatten(t): return [item for sublist in t for item in sublist]

def filter_from_compounds(word_set):
    compounds = []
    for i in range(len(word_set)):
        if len(word_set[i]) <= 2:
            continue

        for j in range(len(word_set)):
            if i == j or len(word_set[j]) <= 2:
                continue

            if abs(len(word_set[i]) - len(word_set[j])) > 2:
                if word_set[i] in word_set[j]:
                    compounds.append(word_set[j])
                elif word_set[j] in word_set[i]:
                    compounds.append(word_set[i])

    return (list(filter(lambda x: x not in compounds, word_set)), compounds)


def get_compound_word_set(word_set: set):
    return list(filter(lambda x: x not in word_set, get_compound_words_recursive('', filter_from_compounds(list(word_set))[0])))


def get_compound_words_recursive(word: str, word_set: list):
    output = list(filter(lambda x: x != None, [word + word_set[i] if len(
        word_set[i]) > 2 and word_set[i] not in word else None for i in range(len(word_set))]))
    
    return output + flatten(list(map(lambda x: get_compound_words_recursive(x, word_set), output)))


def is_compound(word, word_set):
    compounds = get_compound_word_set(word_set)
    return word in compounds


def longest_compound_word(word_set):
    compounds = filter_from_compounds(list(word_set))[1]

    if len(compounds) == 0:
        return None
    
    output_set = [compounds[0]]
    for word in compounds:
        if len(word) > len(output_set[0]):
            output_set = [word]
        elif len(word) == len(output_set[0]):
            output_set.append(word)

    return set(output_set)


def test_one_subwords():
    word_set = set(['fire'])
    assert not is_compound('fire', word_set)


def test_two_subwords():
    word_set = set(['fire',  'man'])
    assert is_compound('fireman', word_set)


def test_three_subwords():
    word_set = set(['news',  'paper',  'man'])
    assert is_compound('newspaperman', word_set)


def test_prefix_is_too_short():
    word_set = set(['a',  'typical'])
    assert not is_compound('atypical', word_set)


def test_suffix_is_too_short():
    word_set = {'or', 'react'}
    assert not is_compound('reactor', word_set)


def test_infix_is_too_short():
    word_set = {'o', 'reflex', 'graph'}
    assert not is_compound('reflexograph', word_set)


def test_prefix_is_invalid():
    word_set = {'law', 'suit'}
    assert not is_compound('prelawsuit', word_set)


def test_suffix_is_invalid():
    word_set = {'over', 'work'}
    assert not is_compound('overworking', word_set)


def test_infix_is_invalid():
    word_set = set(['news',  'man'])
    assert not is_compound('newspaperman', word_set)


def test_backtrack_if_prefix_is_too_short():
    word_set = {'fir', 'fire', 'man'}
    assert is_compound('fireman', word_set)


def test_backtrack_if_prefix_is_too_long():
    word_set = {'snow', 'snows', 'storm'}
    assert is_compound('snowstorm', word_set)


def test_backtrack_if_suffix_is_too_short():
    word_set = {'light', 'house', 'use'}
    assert is_compound('lighthouse', word_set)


def test_backtrack_if_suffix_is_too_long():
    word_set = {'stop', 'light', 'plight'}
    assert is_compound('stoplight', word_set)


def test_backtrack_if_infix_is_incorrect():
    word_set = {'spear', 'mint', 'arm'}
    assert is_compound('spearmint', word_set)


def test_circumfix_is_not_subword():
    word_set = {'peat', 'reed'}
    assert not is_compound('repeated', word_set)


def test_empty_word_set():
    word_set = set()
    assert longest_compound_word(word_set) is None


def test_find_longest():
    word_set = set(['egg',     'head', 'egghead',
                    'police',  'man',  'policeman'])
    assert longest_compound_word(word_set) == {'policeman'}


def test_is_compound_performance():
    word_list = [x.strip().split(" , ")
                for x in open('./fireman_word_set.txt').readlines()]
    word_list = [y.lower() for x in word_list for y in x]
    word_set = set(word_list)
    assert longest_compound_word(word_set) == {
        'supersensitive', 'superstructure'}
