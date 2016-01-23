""" Module qui gère les labels des colonnes """

import string

ALPHABET = string.ascii_uppercase


def add(labels, n):  # Ajoute n labels a la liste labels
    for _ in range(n):
        k = 0 if len(labels) == 0 else len(labels)
        if k < len(ALPHABET):
            label = ALPHABET[k]
        else:
            label = labels[k // len(ALPHABET) - 1] + ALPHABET[k % len(ALPHABET)]
        labels.append(label)


# Genere une liste des n premiers labels
def generate(n):
    l = []
    add(l, n)
    return l


 # Renvoie le label de la colonne c à partir de la liste de labels déja crées pour minimiser les calculs
def getLabel(labels, c):
    try:
        return labels[c - 1]
    except IndexError:
        add(labels, c - len(labels))
        return labels[c - 1]


# Renvoie le numero de colonne ayant pour label n
def getColumn(n):
    if len(n) == 0:
        return 0
    if len(n) == 1:
        return ALPHABET.index(n) + 1
    else:
        return len(ALPHABET) * getColumn(n[:-1]) + ALPHABET.index(n[-1]) + 1
