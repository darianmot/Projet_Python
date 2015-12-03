import visu.columns_labels as columns_labels,structures,cells_traitements.functions as functions,math


OPERATEUR_MATH=['+','-','*','/','//','**']
OPERATEUR_LOG=['<','>','==','<=','>=','!=']
OUVRANTES=['(','{']
FERMANTES=[')','}']
SEPARATEURS=[',',';']

#Renvoie True si l'entrée correspond à une celulle
def isCell(chaine):
    if (chaine[0] not in columns_labels.ALPHABET) or not(chaine[-1].isdigit()): #Le code d'une cellule commence par une lettre et finie par un chiffre
        return False
    in_letters=True    #Si in_letters est vérifiée, on est dans la partie des lettres.
    for char in chaine[1:]:
        if (in_letters==False) and (char in columns_labels.ALPHABET): #S'il existe un chiffre placé avant une lettre, ce n'est pas une celulle
            return False
        elif char in columns_labels.ALPHABET: pass
        elif char.isdigit():
            in_letters=False
        else:                 #Si ce n'est ni un chiffre ni un lettre
            return False
    return True

#Renvoie True si l'entrée correspond syntaxiquement à une fonction
def isfunction(chaine):
    for char in chaine:
        if not(char.isalpha() or char=='_'): #On considere que le nom d'une fonction n'est composé que de lettres de underscore
            return False
    return True

#Renvoie le type, s'il est connu, d'une chaine de caractère
def what_type(chaine):
    if chaine.isdigit():
        return 'entier'
    elif chaine in OPERATEUR_MATH:
        return 'op_math'
    elif chaine in OPERATEUR_LOG:
        return 'op_log'
    elif chaine in OUVRANTES:
        return 'p_ouvrante'
    elif chaine in FERMANTES:
        return 'p_fermante'
    elif chaine in SEPARATEURS:
        return 'sep'
    elif isCell(chaine):
        return 'cell'
    elif isfunction(chaine):
        return 'function'
    else:
        return None

#Découpe en éléments une chaine à traiter et renvoie la liste de ces éléments, ainsi que la liste de leurs types respectifs
def decompo(chaine):
    chaine=chaine.replace(' ','')  #Supprime les espaces
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
                print('Chaine non reconnue:'+str(currentChain)+str(k))

        if (type!=None and k+1==len(chaine)):
            elementList.append(currentChain)
            elementListType.append(type)
    return (elementList,elementListType)
#
# knownFunctions=functions.Knownfunctions()
# knownFunctions.add(functions.Function('f','2*args[0]+args[1]',0))
# knownFunctions.add(functions.Function('cos','math.cos(args[0])',0))

#Renvoie l'évaluation d'une fonction en position k dans une liste d'element
def eval_function(network,elementList,elementType,k):
    element=elementList[k]
    if element not in knownFunctions.dict:  #Si la fonction n'est pas connue, on renvoie une erreur
        return 'Erreur : {} n\'est pas connue'.format(elementList[k])
    if elementType[k+1]!='p_ouvrante':
        return 'Erreur de syntaxe : parenthese'
    p_count=1    #Pour verifier le parenthesage
    args=[]
    currentArg=""
    k+=2
    while p_count>0 and k<len(elementList):
        if elementType[k]=='function':  #Si c'est une fonction, on l'évalue recursivement
            (value,k)=eval_function(network,elementList,elementType,k)
            args.append(value)
            currentArg=""
        elif elementType[k]=='sep':
            if currentArg=="":  #S'il n'y a rien avant un separateur, la syntaxe n'est pas correcte
                return 'Erreur de syntaxe : separateur'
            else:
                args.append(evaluation(network,currentArg))
                currentArg=""
        elif elementType[k]=='p_fermante':  #On gère le parenthesage
            p_count-=1
            if p_count>0:
                currentArg+=elementList[k]
        elif elementType[k]=='p_ouvrante':
            p_count+=1
            currentArg+=elementList[k]
        else:
            currentArg+=elementList[k]
        k+=1
    if currentArg!="":
        args.append(evaluation(network,currentArg))
    return (knownFunctions.dict[str(element)].value(args),k-1)

#Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork (ou affiche l'erreur le cas écheant)
def evaluation(network, chaine):
    chaine_elm=decompo(chaine)[0]
    chaine_type=decompo(chaine)[1]
    i=0
    while i<len(chaine_elm):
        if chaine_type[i]== 'cell':
            chaine_elm[i]=str(network.getCellByName(chaine_elm[i]).value)
        elif chaine_type[i]=='function':
            (value,end)=eval_function(network,chaine_elm,chaine_type,i)
            chaine_elm[i:end+1]=[str(value)]
            i=end
        i+=1
    return eval(''.join(chaine_elm))


# grille=structures.network()
# grille.addColumns(10)
# grille.addRows(10)
# grille.getCell(0,0).value=math.pi
# grille.getCell(0,1).value=2
# print(evaluation(grille,'(A2)*3+f(A2,3**2/2)'))