import visu.columns_labels as columns_labels,structures

OPERATEUR_MATH=['+','-','*','/','//','**']
OPERATEUR_LOG=['<','>','==','<=','>=','!=']
OUVRANTES=['(','[','{']
FERMANTES=[')',']','}']

#Renvoie True si l'entrée correspond à une celulle
def isCell(chaine):
    if (chaine[0] not in columns_labels.ALPHABET) or not(chaine[-1].isdigit()): #Le code d'une cellule commence par une lettre et finie par un chiffre
        return False
    partie1=True    #Si partie1 est vérifiée, on est dans la premiere partie du code de la celulle, ie dans la partie des lettres.
    for char in chaine[1:]:
        if (partie1==False) and (char in columns_labels.ALPHABET): #S'il existe un chiffre placé avant une lettre, ce n'est pas une celulle
            return False
        elif char in columns_labels.ALPHABET: pass
        elif char.isdigit():
            partie1=False
        else:                 #Si ce n'est ni un chiffre ni un lettre
            return False
    return True

#Renvoie True si l'entrée correspond à une fonction (du tableur) [A AJUSTER PLUS TARD]
def isfunction(chaine):
    for char in chaine:
        if not(char.isalpha() or char=='_'): #On considere que le nom d'une fonction n'est composé que de lettres de underscore
            return False
    return True

#Renvoie le type, s'il est connu, d'une chaine de caractère
def what_type(chaine):
    if chaine.isdigit():
        return 'entier'
    if chaine in OPERATEUR_MATH:
        return 'op_math'
    elif chaine in OPERATEUR_LOG:
        return 'op_log'
    elif chaine in OUVRANTES:
        return 'p_ouvrante'
    elif chaine in FERMANTES:
        return 'p_fermante'
    elif isCell(chaine):
        return 'cell'
    elif isfunction(chaine):
        return 'function'
    else:
        return None

#Découpe en éléments une chaine à traiter et renvoie la liste de ces éléments, ainsi que la liste de leurs type respectif
def decompo(chaine):
    elementList=[]
    elementListType=[]
    currentChain=""
    type=None
    for k in range(len(chaine)):
        oldResult=(currentChain,type)
        currentChain+=chaine[k]
        type=what_type(currentChain)
        if type==None:
            if oldResult[1]!=None:
                elementList.append(oldResult[0])
                elementListType.append(oldResult[1])
                currentChain=chaine[k]
                type=what_type(currentChain)
            else:
                print('Chaine non reconnue')
        if (type!=None and k+1==len(chaine)):
            elementList.append(currentChain)
            elementListType.append(type)
    return (elementList,elementListType)

def evaluation(network,chaine):#Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork
    chaine_elm=decompo(chaine)[0]
    chaine_type=decompo(chaine)[1]
    for k in range(len(chaine_elm)):
        if chaine_type[k]== 'cell':
            chaine_elm[k]=str(network.getCellByName(chaine_elm[k]).value)
        if chaine_type[k]=='function':
            pass                        #A Ajuster
    return eval(''.join(chaine_elm))

#Exemple
# grille=structures.network()
# grille.addColumns(10)
# grille.addRows(10)
# grille.getCell(0,0).value=50
# grille.getCell(0,1).value=2
# print(evaluation(grille,'(A1+A2)*3'))