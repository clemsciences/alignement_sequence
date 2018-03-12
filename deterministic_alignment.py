# -*-coding:utf-8-*-

"""
Algorithms implemented here are originally for the French Linux magazine.
"""

import enum
import numpy as np

__author__ = "Clément Besnier <clemsciences@aol.com>"

alphabet_adn = list('acgt')
human_alphabet = list('azertyuiopqsfghjklmwxcvbn')


class States(enum.IntEnum):
    MATCHING = 0
    INSERTION = 1
    DELETION = 2


def align_needleman_wunsch(chi, psi, replacement_matrix, penalty_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_weights = np.zeros((n + 1, m + 1))
    mat_origin = np.zeros((n + 1, m + 1))
    mat_weights[:, 0] = np.array([-i * penalty_is for i in range(n + 1)])
    mat_origin[1:, 0] = 1
    mat_weights[0, :] = np.array([-j * penalty_is for j in range(m + 1)])
    mat_origin[0, 1:] = 2
    # forward
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            propositions = np.array([mat_weights[i - 1, j - 1] +
                                     replacement_matrix[alphabet.index(chi[i - 1]), alphabet.index(psi[j - 1])],
                                     mat_weights[i - 1, j] - penalty_is,
                                     mat_weights[i, j - 1] - penalty_is])
            mat_weights[i, j] = np.max(propositions)
            mat_origin[i, j] = np.argmax(propositions)
    # backward
    chi_alignment = []
    psi_alignment = []
    alignment = []
    i, j = n, m
    while i > 0 or j > 0:
        ori = mat_origin[i, j]
        # print(i, j, ori)
        if ori == States.MATCHING and i > 0 and j > 0:
            i, j = i - 1, j - 1
            chi_alignment.append(chi[i])
            psi_alignment.append(psi[j])
            alignment.append("C")
        elif ori == States.INSERTION and i > 0:
            i -= 1
            chi_alignment.append(chi[i])
            psi_alignment.append("-")
            alignment.append("I")
        elif ori == States.DELETION and j > 0:
            j -= 1
            alignment.append("S")
            chi_alignment.append("-")
            psi_alignment.append(psi[j])
    chi_alignment.reverse()
    psi_alignment.reverse()
    alignment.reverse()
    # print(mat_poids)
    # print(mat_origine)
    return chi_alignment, psi_alignment, alignment


def align_smith_waterman(chi, psi, replacement_matrix, penalty_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_weights = np.zeros((n + 1, m + 1))
    mat_origin = np.zeros((n + 1, m + 1))
    mat_weights[:, 0] = np.array([-i * penalty_is for i in range(n + 1)])
    mat_origin[1:, 0] = 1
    mat_weights[0, :] = np.array([-j * penalty_is for j in range(m + 1)])
    mat_origin[0, 1:] = 2

    # forward
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            propositions = np.array([mat_weights[i - 1, j - 1] +
                                     replacement_matrix[alphabet.index(chi[i - 1]), alphabet.index(psi[j - 1])],
                                     mat_weights[i - 1, j] - penalty_is,
                                     mat_weights[i, j - 1] - penalty_is,
                                     0])
            mat_weights[i, j] = np.max(propositions)
            mat_origin[i, j] = np.argmax(propositions)
    # backward
    chi_alignement = []
    psi_alignement = []
    alignement = []
    # print(mat_poids)
    a = np.unravel_index(mat_weights.argmax(), mat_weights.shape)
    # print("a", a)
    i, j = a
    while mat_weights[i, j] > 0:
        ori = mat_origin[i, j]
        if ori == States.MATCHING and i > 0 and j > 0:
            i, j = i - 1, j - 1
            chi_alignement.append(chi[i])
            psi_alignement.append(psi[j])
            alignement.append("C")
        elif ori == States.INSERTION and i > 0:
            i, j = i - 1, j
            chi_alignement.append(chi[i])
            psi_alignement.append("-")
            alignement.append("I")
        elif ori == States.DELETION and j > 0:
            i, j = i, j - 1
            alignement.append("S")
            chi_alignement.append("-")
            psi_alignement.append(psi[j])
    chi_alignement.reverse()
    psi_alignement.reverse()
    alignement.reverse()
    return chi_alignement, psi_alignement, alignement


def levenshtein_distance(chi, psi, replacement_matrix, penalty_is, alphabet):
    # initialisation
    n, m = len(chi), len(psi)
    mat_weights = np.zeros((n + 1, m + 1))
    mat_weights[:, 0] = np.array([i for i in range(n + 1)])
    mat_weights[0, :] = np.array([j for j in range(m + 1)])
    # forward
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            propositions = np.array([mat_weights[i - 1, j - 1] +
                                     replacement_matrix[alphabet.index(chi[i - 1]), alphabet.index(psi[j - 1])],
                                     mat_weights[i - 1, j] + penalty_is,
                                     mat_weights[i, j - 1] + penalty_is])
            mat_weights[i, j] = np.min(propositions)
    # print(mat_poids)
    return mat_weights[n, m]


if __name__ == "__main__":
    # sequence_1, sequence_2 = "aagtagccactag", "ggaagtaagct"
    sequence_1, sequence_2 = "aggtac", "acgac"
    matrice_log_odds = np.array([[5, -1, -1, -1], [-1, 5, -1, -1], [-1, -1, 5, -1], [-1, -1, -1, 5]])
    d = 0.5
    ali1, ali2, ali = align_needleman_wunsch(sequence_1, sequence_2, matrice_log_odds, d, alphabet_adn)
    print("", "".join(ali1), "\n", "".join(ali2), "\n", "".join(ali))
    # aligner_smith_waterman(sequence_1, sequence_2, matrice_log_odds, d)

    sequence_3 = "aaaaaaaaaatgtcattaaaaaaaa"
    sequence_4 = "ttttgtactggggggggggg"
    ali1, ali2, ali = align_smith_waterman(sequence_3, sequence_4, matrice_log_odds, d, alphabet_adn)
    print("", "".join(ali1), "\n", "".join(ali2), "\n", "".join(ali))
    matrice_levenshtein = np.ones((len(human_alphabet), len(human_alphabet))) + -1 * np.eye(len(human_alphabet))
    print(levenshtein_distance(sequence_1, sequence_2, matrice_levenshtein, 1, human_alphabet))
    print(levenshtein_distance(sequence_3, sequence_4, matrice_levenshtein, 1, human_alphabet))
    print(levenshtein_distance("niche", "chiens", matrice_levenshtein, 1, human_alphabet))
    human_matrix = -5 * np.ones((len(human_alphabet), len(human_alphabet))) + \
                   6 * np.eye(len(human_alphabet))
    print(align_needleman_wunsch("chiens", "niche", human_matrix, d, human_alphabet))
