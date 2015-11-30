import visu.columns_labels as columns_labels

class Cell(object): #caractéristiques et organisation d'une cellule
    def __init__(self,input):
        self.input = input
        self.value = None
        self.name = None     #chaine de caractères
        self.neighbours = []             #liste des cellules dépendant de celle-ci

    def __repr__(self):
        return str(self.name)


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
#


class network(object): #On classe par coordonnées
    def __init__(self):
        self.labels=columns_labels.generate(1)
        self.matrix=[[Cell(None)]]
        self.columnNumber=1
        self.rowNumber=1

    def addRow(self):
        l=[]
        for c in range(self.columnNumber):
            l.append(Cell(None))
            l[-1].name=self.labels[c]+str(self.rowNumber)
        self.matrix.append(l)
        self.rowNumber+=1

    def addRows(self,n):
        for _ in range(n):
            self.addRow()

    def addColumn(self):
        columns_labels.add(self.labels,1)
        for r in range(self.rowNumber):
            self.matrix[r].append(Cell(None))
            self.matrix[r][-1].name=self.labels[self.columnNumber]+str(r)
        self.columnNumber+=1

    def addColumns(self,n):
        for _ in range(n):
            self.addColumn()

    def __repr__(self):
        return str(self.matrix)
