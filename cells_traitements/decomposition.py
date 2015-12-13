import visu.columns_labels as columns_labels,structures,cells_traitements.functions as functions

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

def isNumber(chaine):
    dotNumber=0
    for char in chaine:
        if char == '.':
            dotNumber+=1
        if dotNumber>1 or not(char.isdigit() or char=='.'):
            return False
    return True

def isError(chaine):
    return True if chaine[0]=='#' else False

#Renvoie le type, s'il est connu, d'une chaine de caractère
def what_type(chaine):
    if isNumber(chaine):
        return 'nombre'
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
        if (type!=None and k+1==len(chaine)):
            elementList.append(currentChain)
            elementListType.append(type)
    return (elementList,elementListType)


#Renvoie la position de la parenthese fermant une fonction de position de k dans une liste d'élement
def endOfFunction(elementList,k):
    p_count=0
    for i in range(k+1,len(elementList)):
        if elementList[i] in FERMANTES:
            p_count-=1
        elif elementList[i] in OUVRANTES:
            p_count+=1
        if p_count==0:
            return i
    return len(elementList)-1

#Renvoie l'évaluation d'une fonction en position k dans une liste d'element
def eval_function(network,elementList,elementType,k,knownFunctions):
    element=elementList[k]
    if element not in knownFunctions.dict:  #Si la fonction n'est pas connue, on renvoie une erreur
        return '#Error : {} n\'est pas connue'.format(elementList[k])
    if elementType[k+1]!='p_ouvrante':
        return '#Syntaxe Error : parenthese ouvrante manquante'
    p_count=1    #Pour verifier le parenthesage
    args=[]
    currentArg=""
    k+=2
    while p_count>0 and k<len(elementList):
        if elementType[k]=='function':  #Si c'est une fonction, on l'évalue recursivement
            value=eval_function(network,elementList,elementType,k,knownFunctions)
            if isError(str(value)):
                return value
            k=endOfFunction(elementList,k)
            args.append(value)
            currentArg=""
        elif elementType[k]=='sep':
            if currentArg=="":  #S'il n'y a rien avant un separateur, la syntaxe n'est pas correcte
                return '#Syntax Error : separateur'
            else:
                args.append(evaluation(network,currentArg,knownFunctions))
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
    if p_count!=0:
        return "#Syntax Error : parenthesage"
    if currentArg!="":
        args.append(evaluation(network,currentArg,knownFunctions))
    return knownFunctions.dict[str(element)].value(args)


#Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork (ou affiche l'erreur le cas écheant)
def evaluation(network, chaine,knownFunctions):
    (elementList,elementType)=decompo(chaine)
    i=0
    while i<len(elementList):
        if elementType[i]== 'cell':
            elementList[i]=str(network.getCellByName(elementList[i]).value)
        elif elementType[i]=='function':
            value=eval_function(network,elementList,elementType,i,knownFunctions)
            if isError(str(value)):
                return value
            end=endOfFunction(elementList,i)
            elementList[i:end+1]=[str(value)]
            elementType[i:end+1]=['nombre']
        i+=1
    try:
        return eval(''.join(elementList))
    except SyntaxError as e:
        return '#Syntax Error : {}'.format(e)
    except ZeroDivisionError:
        return '#Division by zero'
    except Exception as e:
        return '#Error : {}'.format(e)

#Evalue linéairement une liste de cellule
def evalList(cellList,network,knownFunctions):
    try:
        for cell in cellList:
            network.getCellByName(cell.name).value=evaluation(network,cell.input[1:],knownFunctions)
    except AttributeError:
        for cell in cellList:
            network.getCellByName(cell.name).value='#Error : cycle'



#Renvoie la liste des celulles apparaissant dans un string
def parentCells(network,chaine):
    (elementList,elementType)=decompo(chaine)
    l=[]
    for k in range(len(elementList)):
        if elementType[k]=='cell':
            l.append(network.getCellByName(elementList[k]))
    return l

#Renvoie l'ensemble des cellules filles (récursive) d'une cellule
def childrenCellsRec(cell):
    l=[]
    for c in cell.children_cells:
       l.append(c)
       l.append(childrenCellsRec(c))
    return l

