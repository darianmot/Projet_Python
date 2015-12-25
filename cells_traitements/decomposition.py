import visu.columns_labels as columns_labels,structures,cells_traitements.functions as functions

OPERATEUR_MATH=['+','-','*','/','//','**']
OPERATEUR_LOG=['<','>','==','<=','>=','!=']
OUVRANTES=['(','{']
FERMANTES=[')','}']
SEPARATEURS=[',',';']

#Erreur levée lorsqu'on trouve une erreur lors de l'evaluation d'une cellule, que l'on affichera alors dans celle ci
class Error(Exception):
    def __init__(self,reason):
        self.reason=reason
        self.disp='#Error : {}'.format(self.reason)


#Renvoie True si l'entrée correspond à une celulle
def isCell(chaine):
    if len(chaine)<2 or (chaine[0] not in columns_labels.ALPHABET and chaine[0]!='$'): #Le code d'une cellule commence par une lettre ou un $
        return False
    in_letters=True    #Si in_letters est vérifiée, on est dans la partie des lettres.
    dollardCount=1 if chaine[0]=='$' else 0
    for char in chaine[1:]:
        if dollardCount>2:  #Si on trouve plus de 2 $ dans la chaine
            return False
        if (in_letters==False) and (char in columns_labels.ALPHABET): #S'il existe un chiffre placé avant une lettre
            return False
        elif char in columns_labels.ALPHABET: pass
        elif char=='$':      #Si on trouve un dollard, soit on est juste avant les chiffres, soit on est pas une cellule
            if in_letters:
                dollardCount+=1
            else:
                return False
        elif char.isdigit():
            in_letters=False
        else:                 #Si ce n'est ni un chiffre ni un lettre ni un $
            return False
    return  (not in_letters or chaine[-1]=='$') #on vérifie qu'on a bien un chiffre ou un dollard à la fin

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
    elif chaine==':':
        return ':'
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
        raise Error('{} n\'est pas connue'.format(elementList[k]))
    try:
        if elementType[k+1]!='p_ouvrante':
            raise Error('\'(\' attendue après {}'.format(elementList[k]))
    except IndexError:
        raise Error('\'()\' attendue après {}'.format(elementList[k]))
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
                raise Error('\'{}\' innatendue'.format(elementList[k]))
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
        raise Error('parenthesage incorrect')
    if currentArg!="":
        args.append(evaluation(network,currentArg,knownFunctions))
    return knownFunctions.dict[str(element)].value(args)


#Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork (ou affiche l'erreur le cas écheant)
def evaluation(network, chaine,knownFunctions):
    (elementList,elementType)=decompo(chaine)
    i=0
    print(elementList)
    for j in [k for k, l in enumerate(elementList) if l == ':']: #On remplace c1:c2 par les celulles comprises dans le rectancle d'extrémité (c1,c2)
        print('on y est')
        if j==0: raise Error('Syntaxe (\':\' innatendue 1)')
        if elementType[j-1]!='cell' or elementType[j+1]!='cell':
            raise Error('Syntaxe (\':\' innatendue 2)')
        try:
            c1=network.getCellByName(elementList[j-1])
            c2=network.getCellByName(elementList[j+1])
        except Error as e:
            raise Error(e.reason)
        cells=cellsBetween(network,c1,c2)
        l_element=[]
        l_type=[]
        for cell in cells:
            l_element.append(cell.name)
            l_type.append('cell')
            if cells.index(cell)<len(cells)-1:
                l_element.append(',')
                l_type.append('sep')
        elementList[j-1:j+2]=l_element
        elementType[j-1:j+2]=l_type
    while i<len(elementList):
        if elementType[i]== 'cell':
            try:
                elementList[i]=str(network.getCellByName(elementList[i]).value)
            except Error as e:
                raise Error(e.reason)
        elif elementType[i]=='function':
            try:
                value=eval_function(network,elementList,elementType,i,knownFunctions)
            except Error as e:
                raise Error(e.reason)
            if isError(str(value)):
                return value
            end=endOfFunction(elementList,i)
            elementList[i:end+1]=[str(value)]
            elementType[i:end+1]=['nombre']
        i+=1
        print(elementList)
    try:
        return eval(''.join(elementList))
    except SyntaxError as e:
        raise Error('Syntaxe ({})'.format(e.msg))
    except ZeroDivisionError:
        raise Error('Division par 0')
    except Exception as e:
        raise Error(str(e))


#Renvoie la liste des celulles apparaissant dans un string
def parentCells(network,chaine):
    (elementList,elementType)=decompo(chaine)
    l=[]
    for k in range(len(elementList)):
        if elementType[k]=='cell':
            try:
                l.append(network.getCellByName(elementList[k]))
            except Error:
                pass
    return l

#Renvoie l'ensemble des cellules filles (récursive) d'une cellule
def childrenCellsRec(cell):
    l=[]
    for c in cell.children_cells:
       l.append(c)
       l.append(childrenCellsRec(c))
    return l

#Retourne la liste de l'ensemble des cellules comprises dans la selection rectangulaire d'extrémité diagonale (c1,c2)
def cellsBetween(network,c1,c2):
    r_init=min(c1.getRow(),c2.getRow())
    c_init=min(c1.getColumn(),c2.getColumn())
    r_end=max(c1.getRow(),c2.getRow())
    c_end=max(c1.getColumn(),c2.getColumn())
    l=[]
    for r in range(r_init,r_end+1):
        for c in range(c_init,c_end+1):
            l.append(network.getCell(r,c))
    return l

