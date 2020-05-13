# Alignement de séquences

**[English version here](https://github.com/clemsciences/alignement_sequence/tree/english)**

[alignement_deterministe.py](https://github.com/clemsciences/alignement_sequence/blob/master/alignement_deterministe.py)
- algorithme de Needleman-Wunsch : alignement global
- algorithme de Smith-Waterman : alignement local
- distance de Levenshtein : nombre d'opérations (ajout, suppression, modification) minimal pour passer d'une séquence à une autre


[blast.py](https://github.com/clemsciences/alignement_sequence/blob/master/blast.py) : heuristique pour trouver des alignements locaux dans de très longues chaînes


[main.py](https://github.com/clemsciences/alignement_sequence/blob/master/main.py) : exemples d'usages des algorithmes présentés


[recuperation_donnees.py](https://github.com/clemsciences/alignement_sequence/blob/master/recuperation_donnees.py) : récupérations de mots grâce à nltk 
1. On installe nltk avec # apt-get install nltk
2. On télécharge le corpus Swadesh avec 
```python
>>> import nltk
>>> nltk.download()
```


[utils.py](https://github.com/clemsciences/alignement_sequence/blob/master/utils.py) : quelques fonctions bien utiles mais inclassables
