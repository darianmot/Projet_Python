import visu.columns_labels as columns_labels,cells_traitements.decomposition as decomposition
from PyQt5 import QtWidgets
class Cell(object): #caractéristiques et organisation d'une cellule
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.input = ""
        self.value = None
        self.name = None     #chaine de caractères
        self.children_cells = [] #liste des cellules filles
        self.parent_cells = []
        self.chainDict = {}

    def getRow(self):
        return self.x

    def getColumn(self):
        return self.y

    def addChildCell(self,other):
        if other not in self.children_cells:
            self.children_cells.append(other)

    def removeChildCell(self, cell):
        try:
            self.children_cells.remove(cell)
        except:
            pass

    def updateParents(self,network):
        newparents=decomposition.parentCells(network,self.input)
        for cell in self.parent_cells:
            if cell not in newparents:
                cell.removeChildCell(self)
        for cell in newparents:
            cell.addChildCell(self)
        self.parent_cells=newparents

    def __repr__(self):
        if self.children_cells==[]:
            return '{0}({1},{2})'.format(self.name,self.x,self.y)
        else:
            return '{0}({1},{2}):{3}'.format(self.name,self.x,self.y,self.children_cells)

# class reseau(object):  #On classe par name
#     def __init__(self):
#         self.labels=columns_labels.generate(1)
#         self.dict={self.labels[0]+str(1):Cell(1,1,None)}
#         self.rows=1
#         self.columns=1
#
#     def addCell(self,x,y,name):
#         self.dict[name]=Cell(x,y,None)
#
#     def addRow(self):
#         for c in range(self.columns):
#             self.addCell(c+1,self.rows+1,self.labels[c]+str(self.rows+1))
#         self.rows+=1
#
#     def addRows(self,n):
#         for _ in range(n):
#             self.addRow()
#
#     def addColumn(self):
#         columns_labels.add(self.labels,1)
#         for r in range(self.rows):
#             self.addCell(self.columns+1,r+1,self.labels[self.columns]+str(r+1))
#         self.columns+=1
#
#     def addColumns(self,n):
#         for _ in range(n):
#             self.addColumn()

class network(object): #On classe par coordonnées
    def __init__(self):
        self.labels=columns_labels.generate(1) #Noms des colonnes
        self.matrix=[[Cell(0,0)]] #Initialisation de la matrice
        self.matrix[0][0].name=columns_labels.getLabel(self.labels,0)+str(1)
        self.columnNumber=1
        self.rowNumber=1

    #Ajoute une ligne au network
    def addRow(self):
        l=[]
        self.rowNumber+=1
        for c in range(self.columnNumber):
            l.append(Cell(self.rowNumber-1,c))
            l[-1].name=columns_labels.getLabel(self.labels,c+1)+str(self.rowNumber)
        self.matrix.append(l)

    #Ajoute n lignes au network
    def addRows(self,n):
        for _ in range(n):
            self.addRow()

    #Ajoute une colonne au network
    def addColumn(self):
        self.columnNumber+=1
        for r in range(self.rowNumber):
            self.matrix[r].append(Cell(r,self.columnNumber-1,))
            self.matrix[r][-1].name=columns_labels.getLabel(self.labels,self.columnNumber)+str(r+1)

    #Ajoute n colonnes au network
    def addColumns(self,n):
        for _ in range(n):
            self.addColumn()

    #Renvoie la celulle de coordonnées (x,y)
    def getCell(self,x,y): #Renvoi la cellule (x,y) si elle existe, 0 sinon
        if x<0  or y < 0: return Cell(-1,-1)
        try:
            return self.matrix[x][y]
        except IndexError:
            return Cell(-1,-1)

    #Renvoie la celulle de nom name
    def getCellByName(self,name): #Renvoi la celulle nommée si elle existe, 0 sinon
        name=''.join([char for char in name if char!='$'])  #On enleve les $ eventuels
        letters=""
        numbers=""
        k=0
        try:
            while len(numbers)==0:
                if name[k].isalpha():
                    letters+=name[k]
                else:
                    numbers+=name[k]
                k+=1
            while k<len(name):
                numbers+=name[k]
                k+=1
        except Exception as e:
            raise decomposition.Error('Format de cellule non valide')
        if len(letters)==0 or len(numbers)==0:
            raise decomposition.Error('Format de cellule non valide')
        try:
            return self.getCell(int(numbers)-1,columns_labels.getColumn(letters)-1)
        except Exception:
            raise decomposition.Error('Cellule {} non trouvée'.format(name))

    #Evalue une liste de celulle du network en vérifiant qu'il n'y ait pas de cycle
    def evalList(self,cellList,knownFunctions):
        try:
            for cell in cellList:
                self.getCellByName(cell.name).value=decomposition.evaluation(self,cell.input[1:],knownFunctions)
        except AttributeError:
            for cell in cellList:
                self.getCellByName(cell.name).value='#Error : cycle'

    def subsitute(self, matrix):
        self.matrix=matrix

    def reset(self,initalRows,initalColumns):
        self.__init__()
        self.addColumns(initalColumns-1)
        self.addRows(initalRows-1)



    def __repr__(self):
        return str(self.matrix)
