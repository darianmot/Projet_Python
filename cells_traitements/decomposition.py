import visu.columns_labels as columns_labels, cells_traitements.functions as functions, copy, re

OPERATEUR_MATH = ['+', '-', '*', '/', '//', '**']
OPERATEUR_LOG = ['<', '>', '==', '<=', '>=', '!=']
OUVRANTES = ['(', '{']
FERMANTES = [')', '}']
SEPARATEURS = [',', ';']
SPECIAUX = [':', '=']

CELL_PATTERN = r"^[$]?[{0}]+[$]?[0-9]+$".format(columns_labels.ALPHABET)  # Paterne d'une celulle en regex


# Erreur levée lorsqu'on trouve une erreur lors de l'evaluation d'une cellule, que l'on affichera alors dans celle ci
class Error(Exception):
    def __init__(self, reason):
        self.reason = reason
        self.disp = '#Error : {}'.format(self.reason)


# Permet de savoir si la chaine match le patern
def matchpattern(chaine, patern):
    return not patern.match(chaine) == None


# Renvoie True si l'entrée correspond à une celulle du type A1, $A1, A$1 ou $A$1
def isCell(chaine):
    p = re.compile(CELL_PATTERN)  # On utilise une expression regulière
    return matchpattern(chaine, p)


# Renvoie True si la chaine est un nombre (flottant ou non)
def isNumber(chaine):
    p = re.compile(r"^[0-9]*\.?([0-9])+$")  # Si la chaine est un nombre (flottant ou non)
    return matchpattern(chaine, p)

# Renvoie True si la chaine est une chaine de char
def isString(chaine):
    p = re.compile(r"^['\"][^'\"]*['\"]$")
    return matchpattern(chaine, p)

# Renvoie True si l'entrée correspond syntaxiquement à une fonction
def isfunction(chaine):
    if isCell(chaine) or isNumber(chaine):
        return False
    p = re.compile(r"^\w+$")  # Une fonction peut contenir des lettres, chiffres et '_', sans être une celulle ni un nombre
    return matchpattern(chaine, p)


def isError(chaine):
    return chaine[0] == '#'


# Renvoie le type, s'il est connu, d'une chaine de caractère
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
    elif chaine == ':':
        return ':'
    elif chaine == '=':
        return '='
    elif isCell(chaine):
        return 'cell'
    elif isString(chaine):
        return 'string'
    elif isfunction(chaine):
        return 'function'
    else:
        return 'unknown'


# Ajoute la chaine à la liste des elements et la liste des types (utile pour decompo)
def addchain(elementList, elementType, chaine):
    if len(chaine) > 0:
        elementList.append(chaine)
        elementType.append(what_type(chaine))


# Découpe en éléments une chaine à traiter et renvoie la liste de ces éléments, ainsi que la liste de leurs types respectifs
def decompo(string):
    string = string.replace(' ', '')
    elementList = []
    elementType = []
    currentChain = ""
    nodes = OPERATEUR_MATH + OPERATEUR_LOG + OUVRANTES + FERMANTES + SEPARATEURS + SPECIAUX
    i = 0
    while i < len(string):
        if string[i] in nodes:  # On decoupe la chaine entre les caractères types +,-,<,; etc...
            addchain(elementList, elementType, currentChain)
            if i == len(string) - 1:  # On regarde si le 'separateur' est composé de 1 ou 2 caractère
                addchain(elementList, elementType, string[i])
            elif string[i] + string[i + 1] in nodes:
                addchain(elementList, elementType, string[i] + string[i + 1])
                i += 1
            else:
                addchain(elementList, elementType, string[i])
            currentChain = ""
        elif i == len(string) - 1:
            addchain(elementList, elementType, currentChain + string[i])
        else:
            currentChain += string[i]
        i += 1
    return (elementList, elementType)


# Renvoie la position de la parenthese fermant une fonction de position de k dans une liste d'élement
def endOfFunction(elementList, k):
    p_count = 0
    for i in range(k + 1, len(elementList)):
        if elementList[i] in FERMANTES:
            p_count -= 1
        elif elementList[i] in OUVRANTES:
            p_count += 1
        if p_count == 0:
            return i
    return len(elementList) - 1

# Remplace (sur place) c1:c2 par les celulles comprises dans le rectancle d'extrémité (c1,c2)
def doublePoint(elementList, elementType, network):
    j = 0
    while j < len(elementList):
        if elementList[j] == ':':
            if j == 0: raise Error('Syntaxe (\':\' innatendue 1)')
            if elementType[j - 1] != 'cell' or elementType[j + 1] != 'cell':
                raise Error('Syntaxe (\':\' innatendue 2)')
            try:
                c1 = network.getCellByName(elementList[j - 1])
                c2 = network.getCellByName(elementList[j + 1])
            except Error as e:
                raise Error(e.reason)
            cells = cellsBetween(network, c1, c2)
            l_element = []
            l_type = []
            for cell in cells:
                l_element.append(cell.name)
                l_type.append('cell')
                if cells.index(cell) < len(cells) - 1:
                    l_element.append(',')
                    l_type.append('sep')
            elementList[j - 1:j + 2] = l_element
            elementType[j - 1:j + 2] = l_type
        j += 1

# Renvoie la liste des celulles apparaissant dans un string
def parentCells(network, chaine):
    if chaine == "":
        return []
    elif chaine[0] != '=':
        return []
    else:
        (elementList, elementType) = decompo(chaine)
        doublePoint(elementList, elementType, network)
        l = []
        for k in range(len(elementList)):
            if elementType[k] == 'cell':
                try:
                    l.append(network.getCellByName(elementList[k]))
                except Error:
                    pass
        return l


# Retourne la liste de l'ensemble des cellules comprises dans la selection rectangulaire d'extrémité diagonale (c1,c2)
def cellsBetween(network, c1, c2):
    r_init = min(c1.getRow(), c2.getRow())
    c_init = min(c1.getColumn(), c2.getColumn())
    r_end = max(c1.getRow(), c2.getRow())
    c_end = max(c1.getColumn(), c2.getColumn())
    l = []
    for r in range(r_init, r_end + 1):
        for c in range(c_init, c_end + 1):
            l.append(network.getCell(r, c))
    return l
