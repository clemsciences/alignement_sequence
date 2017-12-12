# -*-coding:utf-8-*-


import numpy as np

from utils import *
import recuperation_donnees as rd
import alignement_deterministe as ad
import alignement_phmm as ap


__author__ = "besnier"


def script1():
    l_couples_ger = rd.liste_vers_paires(rd.ger)
    ap.em_phmm_alphabeta(l_couples_ger)


def test_genetique():
    sequence = """TCAGACCGTTCATACAGAATTGGCGATCGTTCGGCGTATCGCCGAAATCACCGCCGTAAGCCGACCAGGGGTTGCCGTTA
    TCATCATATTTAATCAGCGACTGATCCACGCAGTCCCAGACGAAGCCGCCCTGTAAACGGGGATACTGACGAAACGCCTG
    CCAGTATTTAGCGAAACCGCCAAGACTGTTACCCATCGCGTGGGCGTATTCGCAAAGGATCAGCGGGCGCGTCTCTCCAG
    GTAGCGATAGCCAATTTTTGATGGACCATTTCGGCACAGCCGGTAAGGGCTGGTCTTCTTCCACGCGCGCGTACATCGGG
    CAAATAATTTCGGTGGCCGTGGTGTCGGCTCCGCCGCCTTCATACTGCACCGGGCGGGAAGGATCGACAGATTTGATCCA
    GCGATACAGCGCGTCGTGATTAGCGCCGTGGCCTGATTCATTCCCCAGCG"""


def test_linguistique1():
    matrice_levenshtein = np.ones((len(alphabet_humain), len(alphabet_humain))) + -1*np.eye(len(alphabet_humain))
    mots_germaniques, alph = rd.recuperer_vocabulaire(rd.langues_germaniques, rd.normaliser_ger)
    distances = np.zeros((len(mots_germaniques), 3))
    for i in range(len(mots_germaniques)):
        mot_en, mot_de, mot_nl = mots_germaniques[i]
        distances[i, 0] = ad.distance_levenshtein(mot_en, mot_de, matrice_levenshtein, 1, alphabet_humain)
        distances[i, 1] = ad.distance_levenshtein(mot_en, mot_nl, matrice_levenshtein, 1, alphabet_humain)
        distances[i, 2] = ad.distance_levenshtein(mot_de, mot_nl, matrice_levenshtein, 1, alphabet_humain)
    print(np.mean(distances, axis=0))
        # distances[i, 3] = ad.distance_levenshtein(mot_en, mot_sw, matrice_levenshtein, 1, alphabet_humain)
        # distances[i, 4] = ad.distance_levenshtein(mot_sw, mot_nl, matrice_levenshtein, 1, alphabet_humain)
        # distances[i, 5] = ad.distance_levenshtein(mot_de, mot_sw, matrice_levenshtein, 1, alphabet_humain)


def test_linguistique2():
    matrice_remplacement = -5*np.ones((len(alphabet_humain), len(alphabet_humain))) + 6*np.eye(len(alphabet_humain))
    mots_germaniques, alph = rd.recuperer_vocabulaire(rd.langues_germaniques, rd.normaliser_ger)
    alignements = []
    for i in range(len(mots_germaniques)):
        mot_en, mot_de, mot_nl = mots_germaniques[i]
        alignements.append([])
        alignements[i].append(ad.aligner_needleman_wunsch(mot_en, mot_de, matrice_remplacement, 1, alphabet_humain))
        alignements[i].append(ad.aligner_needleman_wunsch(mot_en, mot_nl, matrice_remplacement, 1, alphabet_humain))
        alignements[i].append(ad.aligner_needleman_wunsch(mot_de, mot_nl, matrice_remplacement, 1, alphabet_humain))
    print(alignements)


def test_linguistique3():
    matrice_remplacement = -5*np.ones((len(alphabet_humain), len(alphabet_humain))) + 6*np.eye(len(alphabet_humain))
    alignements = []
    mots_romans, alph = rd.recuperer_vocabulaire(rd.langues_romanes, rd.normaliser_rom)
    for i in range(len(mots_romans)):
        mot_fr, mot_es, mot_it = mots_romans[i]
        alignements.append([])
        alignements[i].append(ad.aligner_needleman_wunsch(mot_fr, mot_es, matrice_remplacement, 1, alphabet_humain))
        alignements[i].append(ad.aligner_needleman_wunsch(mot_fr, mot_it, matrice_remplacement, 1, alphabet_humain))
        alignements[i].append(ad.aligner_needleman_wunsch(mot_es, mot_it, matrice_remplacement, 1, alphabet_humain))
    print(alignements)


def test_linguistique4():
    matrice_levenshtein = np.ones((len(alphabet_humain), len(alphabet_humain))) + -1*np.eye(len(alphabet_humain))
    mots_romans, alph = rd.recuperer_vocabulaire(rd.langues_romanes, rd.normaliser_rom)
    distances = np.zeros((len(mots_romans), 3))
    for i in range(len(mots_romans)):
        mot_fr, mot_es, mot_it = mots_romans[i]
        distances[i, 0] = ad.distance_levenshtein(mot_fr, mot_es, matrice_levenshtein, 1, alphabet_humain)
        distances[i, 1] = ad.distance_levenshtein(mot_fr, mot_it, matrice_levenshtein, 1, alphabet_humain)
        distances[i, 2] = ad.distance_levenshtein(mot_es, mot_it, matrice_levenshtein, 1, alphabet_humain)
    print(np.mean(distances, axis=0))


if __name__ == "__main__":
    # script1()
    test_linguistique1()
    # test_linguistique2()
    # test_linguistique3()
    # test_linguistique4()
