# -*-coding:utf-8-*-

"""
Algorithms implemented here are originally for the French Linux magazine.
"""


import random

__author__ = "Clément Besnier <clemsciences@aol.com>"


def step1(seq_ent, k):
    sub_seqs = []
    taille = len(seq_ent)
    for i in range(taille - k + 1):
        sub_seqs.append(seq_ent[i:i+k])
    return sub_seqs


def step2(sub_seqs, base, k):
    res_alignement = []
    for sub_seqs in sub_seqs:
        for i, seq_base in enumerate(base):
            res_alignement.append([])
            for j in range(len(seq_base) - k + 1):
                if sub_seqs == seq_base[j:j+k]:
                    res_alignement[i].append(j)
    return res_alignement


def generate_sequences(length, alphabet):
    return "".join([random.choice(alphabet) for _ in range(length)])


def sequence_noise(seq, factor):
    """

    :param seq:
    :param factor: float between 0 and 1 which represents proportion of resampled characters
    :return:
    """
    noised_seq = []
    alphabet = set([carac for carac in seq])
    for carac in seq:
        if random.random() < factor:
            noised_seq.append(random.choice(alphabet))
        else:
            noised_seq.append(carac)
    return "".join(noised_seq)


if __name__ == "__main__":
    sequence = "TCAGACCGTTCATACAGAATTGGCGATCGTTCGGCGTATCGCCGAAATCACCGCCGTAAGCCGACCAGGGGTTGCCGTTA"\
    "TCATCATATTTAATCAGCGACTGATCCACGCAGTCCCAGACGAAGCCGCCCTGTAAACGGGGATACTGACGAAACGCCTG"\
    "CCAGTATTTAGCGAAACCGCCAAGACTGTTACCCATCGCGTGGGCGTATTCGCAAAGGATCAGCGGGCGCGTCTCTCCAG"\
    "GTAGCGATAGCCAATTTTTGATGGACCATTTCGGCACAGCCGGTAAGGGCTGGTCTTCTTCCACGCGCGCGTACATCGGG"\
    "CAAATAATTTCGGTGGCCGTGGTGTCGGCTCCGCCGCCTTCATACTGCACCGGGCGGGAAGGATCGACAGATTTGATCCA"\
    "GCGATACAGCGCGTCGTGATTAGCGCCGTGGCCTGATTCATTCCCCAGCG"
    base = ["AGGTAC", "GTCCAT"]
    sous_seqs = step1(sequence, 3)
    print(sous_seqs)
    print(step2(sous_seqs, base, 3))


