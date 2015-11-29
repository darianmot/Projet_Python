
import string


ALPHABET=string.ascii_uppercase

def add(labels,n): #Ajoute n labels a la liste labels
    for _ in range(n):
        k=0 if len(labels)==0 else len(labels)
        if k<len(ALPHABET):
            label=ALPHABET[k]
        else:
            label=labels[k//len(ALPHABET)-1]+ALPHABET[k%len(ALPHABET)]
        labels.append(label)

def generate(n): #Genere une liste de  labels
    l=[]
    add(l,n)
    return l





