# -*-coding:utf-8-*-


import numpy as np

from utils import *
import data_retrieval as rd
import deterministic_alignment as ad
import alignement_phmm as ap


__author__ = "Clément Besnier <clemsciences@aol.com>"


def script1():
    l_couples_ger = rd.list_to_pairs(rd.ger)
    ap.em_phmm_alphabeta(l_couples_ger)


def test_genetique():
    sequence = """TCAGACCGTTCATACAGAATTGGCGATCGTTCGGCGTATCGCCGAAATCACCGCCGTAAGCCGACCAGGGGTTGCCGTTA
    TCATCATATTTAATCAGCGACTGATCCACGCAGTCCCAGACGAAGCCGCCCTGTAAACGGGGATACTGACGAAACGCCTG
    CCAGTATTTAGCGAAACCGCCAAGACTGTTACCCATCGCGTGGGCGTATTCGCAAAGGATCAGCGGGCGCGTCTCTCCAG
    GTAGCGATAGCCAATTTTTGATGGACCATTTCGGCACAGCCGGTAAGGGCTGGTCTTCTTCCACGCGCGCGTACATCGGG
    CAAATAATTTCGGTGGCCGTGGTGTCGGCTCCGCCGCCTTCATACTGCACCGGGCGGGAAGGATCGACAGATTTGATCCA
    GCGATACAGCGCGTCGTGATTAGCGCCGTGGCCTGATTCATTCCCCAGCG"""


def test_linguistics1():
    levenshtein_matrix = np.ones((len(human_alphabet), len(human_alphabet))) + -1 * np.eye(len(human_alphabet))
    germanic_words, alph = rd.vocabulary_retrieve(rd.germanic_languages, rd.normalise_ger)
    distances = np.zeros((len(germanic_words), 3))
    for i in range(len(germanic_words)):
        word_en, word_de, word_nl = germanic_words[i]
        distances[i, 0] = ad.levenshtein_distance(word_en, word_de, levenshtein_matrix, 1, human_alphabet)
        distances[i, 1] = ad.levenshtein_distance(word_en, word_nl, levenshtein_matrix, 1, human_alphabet)
        distances[i, 2] = ad.levenshtein_distance(word_de, word_nl, levenshtein_matrix, 1, human_alphabet)
        # distances[i, 3] = ad.distance_levenshtein(word_en, mot_sw, levenshtein_matrix, 1, alphabet_humain)
        # distances[i, 4] = ad.distance_levenshtein(mot_sw, word_nl, levenshtein_matrix, 1, alphabet_humain)
        # distances[i, 5] = ad.distance_levenshtein(word_de, mot_sw, levenshtein_matrix, 1, alphabet_humain)
    print(np.mean(distances, axis=0))


def test_linguistics2():
    matrice_remplacement = -5*np.ones((len(human_alphabet), len(human_alphabet))) + 6 * np.eye(len(human_alphabet))
    germanic_words, alph = rd.vocabulary_retrieve(rd.germanic_languages, rd.normalise_ger)
    alignements = []
    for i in range(len(germanic_words)):
        word_en, word_de, word_nl = germanic_words[i]
        alignements.append([])
        alignements[i].append(ad.align_needleman_wunsch(word_en, word_de, matrice_remplacement, 1, human_alphabet))
        alignements[i].append(ad.align_needleman_wunsch(word_en, word_nl, matrice_remplacement, 1, human_alphabet))
        alignements[i].append(ad.align_needleman_wunsch(word_de, word_nl, matrice_remplacement, 1, human_alphabet))
    print(alignements)


def test_linguistics3():
    remplacement_matrix = -5*np.ones((len(human_alphabet), len(human_alphabet))) + 6 * np.eye(len(human_alphabet))
    alignments = []
    mots_romans, alph = rd.vocabulary_retrieve(rd.roman_languages, rd.normalise_rom)
    for i in range(len(mots_romans)):
        mot_fr, mot_es, mot_it = mots_romans[i]
        alignments.append([])
        alignments[i].append(ad.align_needleman_wunsch(mot_fr, mot_es, remplacement_matrix, 1, human_alphabet))
        alignments[i].append(ad.align_needleman_wunsch(mot_fr, mot_it, remplacement_matrix, 1, human_alphabet))
        alignments[i].append(ad.align_needleman_wunsch(mot_es, mot_it, remplacement_matrix, 1, human_alphabet))
    print(alignments)


def test_linguistique4():
    matrice_levenshtein = np.ones((len(human_alphabet), len(human_alphabet))) + -1 * np.eye(len(human_alphabet))
    roman_words, alph = rd.vocabulary_retrieve(rd.roman_languages, rd.normalise_rom)
    distances = np.zeros((len(roman_words), 3))
    for i in range(len(roman_words)):
        mot_fr, mot_es, mot_it = roman_words[i]
        distances[i, 0] = ad.levenshtein_distance(mot_fr, mot_es, matrice_levenshtein, 1, human_alphabet)
        distances[i, 1] = ad.levenshtein_distance(mot_fr, mot_it, matrice_levenshtein, 1, human_alphabet)
        distances[i, 2] = ad.levenshtein_distance(mot_es, mot_it, matrice_levenshtein, 1, human_alphabet)
    print(np.mean(distances, axis=0))


if __name__ == "__main__":
    # script1()
    test_linguistics1()
    # test_linguistique2()
    # test_linguistique3()
    # test_linguistique4()
