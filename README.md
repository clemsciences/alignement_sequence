
# Sequence alignment

[deterministic_alignment.py](https://github.com/clemsciences/alignement_sequence/blob/master/deterministic_alignment.py)
- Needleman-Wunsch algorithm: global alignment
- Smith-Waterman algorithm: local alignment
- Levenshtein distance: minimum number of operations (insertion, deletion, modification) to transform one sequence to an other sequence


[blast.py](https://github.com/clemsciences/alignement_sequence/blob/master/blast.py) : heuristics to find local alignmentsin very long chains


[main.py](https://github.com/clemsciences/alignement_sequence/blob/master/main.py) : examples of presented algorithms


[recuperation_donnees.py](https://github.com/clemsciences/alignement_sequence/blob/master/data_retrival.py) : word retrieval thanks to nltk

1. Install nltk with # apt-get install nltk
2. Download Swadesh corpus with
```python
>>> import nltk
>>> nltk.download()
```


[utils.py](https://github.com/clemsciences/alignement_sequence/blob/master/utils.py) : som useful functions which are unclassified
