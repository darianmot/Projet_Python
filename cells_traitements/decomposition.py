import visu.columns_labels as columns_labels,cells_traitements.functions as functions,copy,re

OPERATEUR_MATH=['+','-','*','/','//','**']
OPERATEUR_LOG=['<','>','==','<=','>=','!=']
OUVRANTES=['(','{']
FERMANTES=[')','}']
SEPARATEURS=[',',';']
SPECIAUX=[':','=']

CELL_PATTERN=r"^[$]?[{0}]+[$]?[0-9]+$".format(columns_labels.ALPHABET) #Paterne d'une celulle (regex)

#Erreur levée lorsqu'on trouve une erreur lors de l'evaluation d'une cellule, que l'on affichera alors dans celle ci
class Error(Exception):
    def __init__(self,reason):
        self.reason=reason
        self.disp='#Error : {}'.format(self.reason)

#Permet de savoir si la chaine match le patern
def matchpattern(chaine,patern):
    if patern.match(chaine)==None:
        return False
    else:
        return True

#Renvoie True si l'entrée correspond à une celulle du type A1, $A1, A$1 ou $A$1
def isCell(chaine):
    p=re.compile(CELL_PATTERN) #On utilise une expression regulière
    return matchpattern(chaine,p)

#Renvoie True si l'entrée correspond syntaxiquement à une fonction
def isfunction(chaine):
    p=re.compile(r"^(?!{0})\w+$".format(CELL_PATTERN)) #Une fonction peut contenir des lettres, chiffres et '_', tant que ce n'est pas le nom d'une celulle
    return matchpattern(chaine,p)

def isNumber(chaine):
    p=re.compile(r"^[0-9]*\.?([0-9])+$") #Si la chaine est un nombre flottant
    return matchpattern(chaine,p)

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
    elif chaine=='=':
        return '='
    elif isCell(chaine):
        return 'cell'
    elif isfunction(chaine):
        return 'function'
    else:
        return 'unknown'

#Ajoute la chaine à la liste des elements et la liste des types (utile pour decompo)
def addchain(elementList,elementType,chaine):
    if len(chaine)>0:
        elementList.append(chaine)
        elementType.append(what_type(chaine))

#Découpe en éléments une chaine à traiter et renvoie la liste de ces éléments, ainsi que la liste de leurs types respectifs
def decompo(string):
    string=string.replace(' ','')
    elementList=[]
    elementType=[]
    currentChain=""
    nodes=OPERATEUR_MATH+OPERATEUR_LOG+OUVRANTES+FERMANTES+SEPARATEURS+SPECIAUX
    i=0
    while i<len(string):
        if string[i] in nodes: #On decoupe la chaine entre les caractères types +,-,<,; etc...
            addchain(elementList,elementType,currentChain)
            if i==len(string)-1: #On regarde si le 'separateur' est composé de 1 ou 2 caractère
                addchain(elementList,elementType,string[i])
            elif string[i]+string[i+1] in nodes:
                addchain(elementList,elementType,string[i]+string[i+1])
                i+=1
            else:
                addchain(elementList,elementType,string[i])
            currentChain=""
        elif i==len(string)-1:
            addchain(elementList,elementType,currentChain + string[i])
        else:
            currentChain+=string[i]
        i+=1
    return (elementList,elementType)

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

#Remplace (sur place) c1:c2 par les celulles comprises dans le rectancle d'extrémité (c1,c2)
def doublePoint(elementList,elementType,network):
    for j in [k for k, l in enumerate(elementList) if l == ':']:
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

#Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork (ou affiche l'erreur le cas écheant)
def evaluation(network, chaine,knownFunctions):
    (elementList,elementType)=decompo(chaine)
    i=0
    doublePoint(elementList,elementType,network)
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
    try:
        return eval(''.join(elementList))
    except SyntaxError as e:
        raise Error('Syntaxe ({})'.format(e.msg))
    except ZeroDivisionError:
        raise Error('Division par 0')
    except Exception as e:
        print(''.join(elementList))
        raise Error(str(e))


#Renvoie la liste des celulles apparaissant dans un string
def parentCells(network,chaine):
    (elementList,elementType)=decompo(chaine)
    doublePoint(elementList,elementType,network)
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

# #Renvoie le input à traiter dans la celulle situé rows lignes plus bas que la celulle initale dans le cas où l'utilisateur tire verticalement sur le coin
# def verticalPull(inputDecomposed,rows):
#     elementList=copy.copy(inputDecomposed[0]) #Pour ne pas changer sur place la decomposition initiale
#     elementType=inputDecomposed[1]
#     for i in range(len(elementList)):
#         if elementType[i]=='cell':
#             dollardcount=elementList[i].count("$")
#             if not((dollardcount==1 and elementList[i][0]!='$') or dollardcount==2): #Si il n'y a pas de $ devant la partie numerique
#                 elementList[i]=elementList[i][:-1]+str(int(elementList[i][-1])+rows)
#     return ''.join(elementList)
#
# #Renvoie le input à traiter dans la celulle situé à columns colonnes de la celulle initale dans le cas où l'utilisateur tire horizonatalement sur le coin
# def horizontalPull(inputDecomposed,columns,labels):
#     elementList=copy.copy(inputDecomposed[0]) #Pour ne pas changer sur place la decomposition initiale
#     elementType=inputDecomposed[1]
#     for i in range(len(elementList)):
#         if elementType[i]=='cell':
#             if elementList[i][0]!='$':
#                 letters=''.join([char for char in elementList[i] if char.isalpha()])
#                 n=columns_labels.getColumn(letters)      #On recupere le label de la colonne pour l'itérer columns fois
#                 newletters=columns_labels.getLabel(labels,n+columns)
#                 elementList[i]=newletters+elementList[i][n:]    #On change la partie des lettres
#     return ''.join(elementList)



