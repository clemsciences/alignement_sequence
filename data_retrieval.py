# -*-coding:utf-8-*-

"""
This module is an example for Swadesh corpus retrieval
"""

import re
import numpy as np
from nltk.corpus import swadesh


__author__ = "besnier"

germanic_languages = ["en", "de", "nl"]
roman_languages = ["fr", "es", "it"]
alphabet = list('azertyuiopqsdfghjklmwxcvbn')

to_aligner_ger = swadesh.entries(germanic_languages)
to_aligner_rom = swadesh.entries(roman_languages)


def vocabulary_retrieve(languages, normalize):
    """
    Load and normalize corpora according to chosen languages
    :param languages:
    :param normalize:
    :return:
    """
    to_align = swadesh.entries(languages)
    normalised_words = []
    characters = set()
    for i, mots in enumerate(to_align):
        normalised_words.append([])
        for j in range(len(languages)):
            normalised_words[i].append(list(normalize(mots[j])))
            characters.update(normalised_words[i][j])
    return normalised_words, list(characters)


def normalise_rom(word):
    """
    Normalise French, Spanish and Italian
    :param word:
    :return: normalised word
    """
    if ',' in word:
        i = word.find(',')
        word = word[:i]
    word = re.sub(r' \([\w ]*\)', '', word.lower())
    word = word.replace(' ', '')
    word = word.replace('...', '')
    word = word.replace("'", '')
    word = word.replace('ù', 'u')
    word = word.replace('œ', 'oe')
    word = word.replace('è', 'e')
    word = word.replace('é', 'e')
    word = word.replace('á', 'a')
    word = word.replace('à', 'a')
    word = word.replace('ñ', 'n')
    word = word.replace('í', 'i')
    word = word.replace('â', 'a')
    word = word.replace('ê', 'e')
    word = word.replace('û', 'u')
    word = word.replace('ó', 'o')
    word = word.replace('ú', 'u')
    word = word.replace('ü', 'u')
    return word


def normalise_ger(word):
    """
    Normaliser for western Germanic languages
    :param word:
    :return: normalised_word
    """
    if ',' in word:
        i = word.find(',')
        word = word[:i]
    word = re.sub(r' \([\w ]*\)', '', word.lower()).replace(' ', '')
    word = word.replace('ß', 'ss')
    word = word.replace('ö', 'oe')
    word = word.replace('ü', 'ue')
    word = word.replace('ä', 'ae')
    word = word.replace('á', 'a')
    word = word.replace('à', 'a')
    word = word.replace('í', 'i')
    word = word.replace('â', 'a')
    word = word.replace('ê', 'e')
    word = word.replace('û', 'u')
    word = word.replace('ó', 'o')
    word = word.replace('ú', 'u')
    word = word.replace('å', 'aa')
    return word


def list_to_pairs(l):
    """
    From list(list(str)) ) to list([str, str])
    :param l:
    :return:
    """
    res = []
    for i in l:
        length_i = len(i)
        for j in range(length_i-1):
            for k in range(j+1, length_i):
                res.append([np.array(i[j]), np.array(i[k])])
    return res


if __name__ == "__main__":
    # print(list_to_pairs(ger))
    # print(list_to_pairs(rom))
    vocabulary_retrieve(germanic_languages, normalise_ger)
    vocabulary_retrieve(roman_languages, normalise_rom)
