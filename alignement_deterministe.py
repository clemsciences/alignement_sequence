# -*-coding:utf-8-*-

"""
Les algorithmes implémentés apparaissent dans un article de Linux magazine
"""

import enum
import numpy as np

__author__ = "besnier"

alphabet_adn = list('acgt')
alphabet_humain = list('azertyuiopqsfghjklmwxcvbn')


class Etats(enum.IntEnum):
    CORRESPONDANCE = 0
    INSERTION = 1
    SUPPRESSION = 2


def aligner_needleman_wunsch(chi, psi, matrice_remplacement, penalite_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_poids = np.zeros((n+1, m+1))
    mat_origine = np.zeros((n+1, m+1))
    mat_poids[:, 0] = np.array([-i*penalite_is for i in range(n+1)])
    mat_origine[1:, 0] = 1
    mat_poids[0, :] = np.array([-j*penalite_is for j in range(m+1)])
    mat_origine[0, 1:] = 2
    # étape prograde
    for i in range(1, n+1):
        for j in range(1, m+1):
            propositions = np.array([mat_poids[i-1, j-1] +
                                     matrice_remplacement[alphabet.index(chi[i-1]), alphabet.index(psi[j-1])],
                                     mat_poids[i-1, j] - penalite_is,
                                     mat_poids[i, j-1] - penalite_is])
            mat_poids[i, j] = np.max(propositions)
            mat_origine[i, j] = np.argmax(propositions)
    # étape rétrograde
    chi_alignement = []
    psi_alignement = []
    alignement = []
    i, j = n, m
    while i > 0 or j > 0:
        ori = mat_origine[i, j]
        # print(i, j, ori)
        if ori == Etats.CORRESPONDANCE and i > 0 and j > 0:
            i, j = i-1, j-1
            chi_alignement.append(chi[i])
            psi_alignement.append(psi[j])
            alignement.append("C")
        elif ori == Etats.INSERTION and i > 0:
            i -= 1
            chi_alignement.append(chi[i])
            psi_alignement.append("-")
            alignement.append("I")
        elif ori == Etats.SUPPRESSION and j > 0:
            j -= 1
            alignement.append("S")
            chi_alignement.append("-")
            psi_alignement.append(psi[j])
    chi_alignement.reverse()
    psi_alignement.reverse()
    alignement.reverse()
    # print(mat_poids)
    # print(mat_origine)
    return chi_alignement, psi_alignement, alignement


def aligner_smith_waterman(chi, psi, matrice_remplacement, penalite_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_poids = np.zeros((n+1, m+1))
    mat_origine = np.zeros((n+1, m+1))
    mat_poids[:, 0] = np.array([-i*penalite_is for i in range(n+1)])
    mat_origine[1:, 0] = 1
    mat_poids[0, :] = np.array([-j*penalite_is for j in range(m+1)])
    mat_origine[0, 1:] = 2

    # étape prograde
    for i in range(1, n+1):
        for j in range(1, m+1):
            propositions = np.array([mat_poids[i-1, j-1] +
                                     matrice_remplacement[alphabet.index(chi[i-1]), alphabet.index(psi[j-1])],
                                     mat_poids[i-1, j] - penalite_is,
                                     mat_poids[i, j-1] - penalite_is,
                                     0])
            mat_poids[i, j] = np.max(propositions)
            mat_origine[i, j] = np.argmax(propositions)
    # étape rétrograde
    chi_alignement = []
    psi_alignement = []
    alignement = []
    # print(mat_poids)
    a = np.unravel_index(mat_poids.argmax(), mat_poids.shape)
    # print("a", a)
    i, j = a
    while mat_poids[i, j] > 0:
        ori = mat_origine[i, j]
        if ori == Etats.CORRESPONDANCE and i > 0 and j > 0:
            i, j = i-1, j-1
            chi_alignement.append(chi[i])
            psi_alignement.append(psi[j])
            alignement.append("C")
        elif ori == Etats.INSERTION and i > 0:
            i, j = i-1, j
            chi_alignement.append(chi[i])
            psi_alignement.append("-")
            alignement.append("I")
        elif ori == Etats.SUPPRESSION and j > 0:
            i, j = i, j-1
            alignement.append("S")
            chi_alignement.append("-")
            psi_alignement.append(psi[j])
    chi_alignement.reverse()
    psi_alignement.reverse()
    alignement.reverse()
    return chi_alignement, psi_alignement, alignement


def distance_levenshtein(chi, psi, matrice_remplacement, penalite_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_poids = np.zeros((n+1, m+1))
    mat_poids[:, 0] = np.array([i for i in range(n+1)])
    mat_poids[0, :] = np.array([j for j in range(m+1)])
    # étape prograde
    for i in range(1, n+1):
        for j in range(1, m+1):
            propositions = np.array([mat_poids[i-1, j-1] +
                                     matrice_remplacement[alphabet.index(chi[i-1]), alphabet.index(psi[j-1])],
                                     mat_poids[i-1, j] + penalite_is,
                                     mat_poids[i, j-1] + penalite_is])
            mat_poids[i, j] = np.min(propositions)
    # print(mat_poids)
    return mat_poids[n, m]

if __name__ == "__main__":
    sequence_1, sequence_2 = "aagtagccactag", "ggaagtaagct"
    matrice_log_odds = np.array([[5, -1, -1, -1], [-1, 5, -1, -1], [-1, -1, 5, -1], [-1, -1, -1, 5]])
    d = 0.5
    ali1, ali2, ali = aligner_needleman_wunsch(sequence_1, sequence_2, matrice_log_odds, d, alphabet_adn)
    print("", "".join(ali1), "\n", "".join(ali2), "\n", "".join(ali))
    # aligner_smith_waterman(sequence_1, sequence_2, matrice_log_odds, d)

    sequence_3 = "aaaaaaaaaatgtcattaaaaaaaa"
    sequence_4 = "ttttgtactggggggggggg"
    ali1, ali2, ali = aligner_smith_waterman(sequence_3, sequence_4, matrice_log_odds, d, alphabet_adn)
    print("", "".join(ali1), "\n", "".join(ali2), "\n", "".join(ali))
    matrice_levenshtein = np.ones((len(alphabet_humain), len(alphabet_humain))) + -1*np.eye(len(alphabet_humain))
    print(distance_levenshtein(sequence_1, sequence_2, matrice_levenshtein, 1, alphabet_humain))
    print(distance_levenshtein(sequence_3, sequence_4, matrice_levenshtein, 1, alphabet_humain))
    print(distance_levenshtein("niche", "chiens", matrice_levenshtein, 1, alphabet_humain))
    mat_humain = -5*np.ones((len(alphabet_humain), len(alphabet_humain))) + \
                                   6*np.eye(len(alphabet_humain))
    print(aligner_needleman_wunsch("chiens", "niche", mat_humain, d, alphabet_humain))
