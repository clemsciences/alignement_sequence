# -*-coding:utf-8-*-


import enum


__author__ = "besnier"

alphabet_humain = list('azertyuiopqsdfghjklmwxcvbn')


etats = ["M", "I", "S"]


def delta(predicat):
    if predicat:
        return 1
    else:
        return 0


class Etats(enum.IntEnum):
    CORRESPONDANCE = 0
    INSERTION = 1
    SUPPRESSION = 2


def liste_vers_paires(l):
    """
    Passer d'une structure en list(list(str)) ) list([str, str])
    :param l:
    :return:
    """
    res = []
    for i in l:
        taille_i = len(i)
        for j in range(taille_i-1):
            for k in range(j+1, taille_i):
                res.append([i[j], i[k]])
    return res


def test_liste_vers_paries():
    l = [[1, 2, 3], [45, 46], [98, 99, 100, 101]]
    res = liste_vers_paires(l)
    print(res)
    assert res == [[1, 2], [1, 3], [2, 3], [45, 46], [98, 99], [98, 100], [98, 101], [99, 100], [99, 101], [100, 101]]


if __name__ == "__main__":
    test_liste_vers_paries()