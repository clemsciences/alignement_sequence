# -*-coding:utf-8-*-

"""
Ce module sert d'exemple pour la récupération du corpus de Swadesh
"""

import re
import numpy as np
from nltk.corpus import swadesh


__author__ = "besnier"

langues_germaniques = ["en", "de", "nl"]
langues_romanes = ["fr", "es", "it"]
alphabet = list('azertyuiopqsdfghjklmwxcvbn')

a_aligner_ger = swadesh.entries(langues_germaniques)
a_aligner_rom = swadesh.entries(langues_romanes)


def recuperer_vocabulaire(langues, normaliser):
    """
    Charger et normaliser les corpus selon les langues choisis
    :param langues:
    :param normaliser:
    :return:
    """
    a_aligner = swadesh.entries(langues)
    mots_normalises = []
    caracteres = set()
    for i, mots in enumerate(a_aligner):
        mots_normalises.append([])
        for j in range(len(langues)):
            mots_normalises[i].append(list(normaliser(mots[j])))
            caracteres.update(mots_normalises[i][j])
    return mots_normalises, list(caracteres)


def normaliser_rom(mot):
    """
    Normaliser le français, l'espagnol et l'italien
    :param mot:
    :return:
    """
    if ',' in mot:
        i = mot.find(',')
        mot = mot[:i]
    mot = re.sub(r' \([\w ]*\)', '', mot.lower())
    mot = mot.replace(' ', '')
    mot = mot.replace('...', '')
    mot = mot.replace("'", '')
    mot = mot.replace('ù', 'u')
    mot = mot.replace('œ', 'oe')
    mot = mot.replace('è', 'e')
    mot = mot.replace('é', 'e')
    mot = mot.replace('á', 'a')
    mot = mot.replace('à', 'a')
    mot = mot.replace('ñ', 'n')
    mot = mot.replace('í', 'i')
    mot = mot.replace('â', 'a')
    mot = mot.replace('ê', 'e')
    mot = mot.replace('û', 'u')
    mot = mot.replace('ó', 'o')
    mot = mot.replace('ú', 'u')
    mot = mot.replace('ü', 'u')
    return mot


def normaliser_ger(mot):
    """
    Normaliseur pour les langues germaniques occidentales
    :param mot:
    :return:
    """
    if ',' in mot:
        i = mot.find(',')
        mot = mot[:i]
    mot = re.sub(r' \([\w ]*\)', '', mot.lower()).replace(' ', '')
    mot = mot.replace('ß', 'ss')
    mot = mot.replace('ö', 'oe')
    mot = mot.replace('ü', 'ue')
    mot = mot.replace('ä', 'ae')
    mot = mot.replace('á', 'a')
    mot = mot.replace('à', 'a')
    mot = mot.replace('ñ', 'n')
    mot = mot.replace('í', 'i')
    mot = mot.replace('â', 'a')
    mot = mot.replace('ê', 'e')
    mot = mot.replace('û', 'u')
    mot = mot.replace('ó', 'o')
    mot = mot.replace('ú', 'u')
    mot = mot.replace('å', 'aa')
    return mot


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
                res.append([np.array(i[j]), np.array(i[k])])
    return res

if __name__ == "__main__":
    # print(liste_vers_paires(ger))
    # print(liste_vers_paires(rom))
    recuperer_vocabulaire(langues_germaniques, normaliser_ger)
    recuperer_vocabulaire(langues_romanes, normaliser_rom)
