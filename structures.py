import cells_traitements.decomposition as decomposition
import visu.columns_labels as columns_labels


# Représente une cellule du tableau
class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.input = ""
        self.value = None
        self.name = None
        self.children_cells = []
        self.parent_cells = []

    def getRow(self):
        return self.x

    def getColumn(self):
        return self.y

    def addChildCell(self, other):
        if other not in self.children_cells:
            self.children_cells.append(other)

    def removeChildCell(self, cell):
        try:
            self.children_cells.remove(cell)
        except:
            print('Can not remove {}'.format(cell))

    def updateParents(self, network):
        newparents = decomposition.parentCells(network, self.input)
        for cell in self.parent_cells:
            if cell not in newparents:
                cell.removeChildCell(self)
        for cell in newparents:
            cell.addChildCell(self)
        self.parent_cells = newparents

    def __repr__(self):
        if not self.children_cells:
            return '{0}({1},{2})'.format(self.name, self.x, self.y)
        else:
            return '{0}({1},{2}):{3}'.format(self.name, self.x, self.y, self.children_cells)


class network(object):  # On classe par coordonnées
    def __init__(self):
        self.labels = columns_labels.generate(1)  # Noms des colonnes
        self.matrix = [[Cell(0, 0)]]  # Initialisation de la matrice
        self.matrix[0][0].name = columns_labels.getLabel(self.labels, 0) + str(1)
        self.columnNumber = 1
        self.rowNumber = 1
        self.saved = True
        self.title = "Nouvelle feuille"

    # Ajoute une ligne au network
    def addRow(self):
        l = []
        self.rowNumber += 1
        for c in range(self.columnNumber):
            l.append(Cell(self.rowNumber - 1, c))
            l[-1].name = columns_labels.getLabel(self.labels, c + 1) + str(self.rowNumber)
        self.matrix.append(l)

    # Ajoute n lignes au network
    def addRows(self, n):
        for _ in range(n):
            self.addRow()

    # Ajoute une colonne au network
    def addColumn(self):
        self.columnNumber += 1
        for r in range(self.rowNumber):
            self.matrix[r].append(Cell(r, self.columnNumber - 1, ))
            self.matrix[r][-1].name = columns_labels.getLabel(self.labels, self.columnNumber) + str(r + 1)

    # Ajoute n colonnes au network
    def addColumns(self, n):
        for _ in range(n):
            self.addColumn()

    # Renvoie la celulle de coordonnées (x,y)
    def getCell(self, x, y):  # Renvoi la cellule (x,y) si elle existe, sinon la cellule Cell(-1,-1) d'erreur
        if x < 0 or y < 0: return Cell(-1, -1)
        try:
            return self.matrix[x][y]
        except IndexError:
            return Cell(-1, -1)

    # Renvoie la celulle de nom name
    def getCellByName(self, name):  # Renvoi la celulle nommée si elle existe, 0 sinon
        name = ''.join([char for char in name if char != '$'])  # On enleve les $ eventuels
        letters = ""
        numbers = ""
        k = 0
        if not decomposition.isCell(name):
            raise decomposition.Error('Format de cellule non valide')
        else:
            while len(numbers) == 0:
                if name[k].isalpha():
                    letters += name[k]
                else:
                    numbers += name[k]
                k += 1
            while k < len(name):
                numbers += name[k]
                k += 1
        try:
            return self.getCell(int(numbers) - 1, columns_labels.getColumn(letters) - 1)
        except Exception:
            raise decomposition.Error('Cellule {} non trouvée'.format(name))

    # Evalue une liste de celulle du network en vérifiant qu'il n'y ait pas de cycle
    def evalList(self, cellList, knownFunctions):
        try:
            for cell in cellList:
                self.getCellByName(cell.name).value = decomposition.evaluation(self, cell.input[1:], knownFunctions)
        except AttributeError:
            for cell in cellList:
                self.getCellByName(cell.name).value = '#Error : cycle'

    def subsitute(self, newmatrix):
        self.matrix = newmatrix
        self.rowNumber = len(newmatrix)
        self.columnNumber = len(newmatrix[0])

    def reset(self, initalRows, initalColumns):
        self.__init__()
        self.subsitute([[Cell(0, 0)]])
        self.getCell(0,0).name = columns_labels.getLabel(self.labels, 0) + str(1)
        self.addColumns(initalColumns - 1)
        self.addRows(initalRows - 1)
        self.columnNumber = initalColumns
        self.rowNumber = initalRows

    def __repr__(self):
        return str(self.matrix)
