# -*-coding:utf-8-*-

"""
Les algorithmes implémentés apparaissent dans un article de Linux magazine
"""


import random

__author__ = "besnier"


def etape1(seq_ent, k):
    sous_seqs = []
    taille = len(seq_ent)
    for i in range(taille - k + 1):
        sous_seqs.append(seq_ent[i:i+k])
    return sous_seqs


def etape2(sous_seqs, base, k):
    res_alignements = []
    for sous_seq in sous_seqs:
        for i, seq_base in enumerate(base):
            res_alignements.append([])
            for j in range(len(seq_base) - k + 1):
                if sous_seq == seq_base[j:j+k]:
                    res_alignements[i].append(j)
    return res_alignements


# def etape3(seq_ent, seq_base, indice, taille, matrice_substitution):
#     score = [-1]*len(seq_base)
#     for i in range(indice, indice+taille):
#         score




def generer_sequences(taille, alphabet):
    return "".join([random.choice(alphabet) for _ in range(taille)])


def bruiter_sequence(seq, facteur):
    """

    :param seq:
    :param facteur: float entre 0 et 1 qui représente la proportion de caractère qui sera remisée
    :return:
    """
    seq_bruitee = []
    alphabet = set([carac for carac in seq])
    for carac in seq:
        if random.random() < facteur:
            seq_bruitee.append(random.choice(alphabet))
        else:
            seq_bruitee.append(carac)
    return "".join(seq_bruitee)

if __name__ == "__main__":
    sequence = "TCAGACCGTTCATACAGAATTGGCGATCGTTCGGCGTATCGCCGAAATCACCGCCGTAAGCCGACCAGGGGTTGCCGTTA"\
    "TCATCATATTTAATCAGCGACTGATCCACGCAGTCCCAGACGAAGCCGCCCTGTAAACGGGGATACTGACGAAACGCCTG"\
    "CCAGTATTTAGCGAAACCGCCAAGACTGTTACCCATCGCGTGGGCGTATTCGCAAAGGATCAGCGGGCGCGTCTCTCCAG"\
    "GTAGCGATAGCCAATTTTTGATGGACCATTTCGGCACAGCCGGTAAGGGCTGGTCTTCTTCCACGCGCGCGTACATCGGG"\
    "CAAATAATTTCGGTGGCCGTGGTGTCGGCTCCGCCGCCTTCATACTGCACCGGGCGGGAAGGATCGACAGATTTGATCCA"\
    "GCGATACAGCGCGTCGTGATTAGCGCCGTGGCCTGATTCATTCCCCAGCG"
    base = ["AGGTAC", "GTCCAT"]
    sous_seqs = etape1(sequence, 3)
    print(sous_seqs)
    print(etape2(sous_seqs, base, 3))


