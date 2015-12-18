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
        self.labels=columns_labels.generate(1)
        self.matrix=[[Cell(0,0)]]
        self.matrix[0][0].name=columns_labels.getLabel(self.labels,0)+str(1)
        self.columnNumber=1
        self.rowNumber=1

    def addRow(self):
        l=[]
        self.rowNumber+=1
        for c in range(self.columnNumber):
            l.append(Cell(self.rowNumber-1,c))
            l[-1].name=columns_labels.getLabel(self.labels,c+1)+str(self.rowNumber)
        self.matrix.append(l)

    def addRows(self,n):
        for _ in range(n):
            self.addRow()

    def addColumn(self):
        self.columnNumber+=1
        for r in range(self.rowNumber):
            self.matrix[r].append(Cell(r,self.columnNumber-1,))
            self.matrix[r][-1].name=columns_labels.getLabel(self.labels,self.columnNumber)+str(r+1)

    def addColumns(self,n):
        for _ in range(n):
            self.addColumn()

    def getCell(self,x,y): #Renvoi la cellule (x,y) si elle existe, 0 sinon
        if x<0  or y < 0: return Cell(-1,-1)
        try:
            return self.matrix[x][y]
        except IndexError:
            return Cell(-1,-1)

    def getCellByName(self,name): #Renvoi la celulle nommée si elle existe, 0 sinon
        letters=""
        numbers=""
        k=0
        while len(numbers)==0:
            if name[k].isalpha():
                letters+=name[k]
            else:
                numbers+=name[k]
            k+=1
        while k<len(name):
            numbers+=name[k]
            k+=1
        try:
            return self.getCell(int(numbers)-1,columns_labels.getColumn(letters)-1)
        except :
            return 0

    def evalList(self,cellList,knownFunctions):
        try:
            for cell in cellList:
                self.getCellByName(cell.name).value=decomposition.evaluation(self,cell.input[1:],knownFunctions)
        except AttributeError:
            for cell in cellList:
                self.getCellByName(cell.name).value='#Error : cycle'
    def __repr__(self):
        return str(self.matrix)
