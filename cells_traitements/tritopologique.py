""" Dans ce module, on s'occupe d'ordonner une liste de celulles à évaluer selon le tri topologique """

#Renvoie l'ensemble des cellules filles (récursive) d'une cellule
# def childrenCellsRec(cell):
#     l=[]
#     for c in cell.children_cells:
#         print(l)
#         if (c not in l) and c!=cell:
#             l.append(c)
#             l+=childrenCellsRec(c)
#     return l
def childrenCellsRec(parent):
    file=[parent]
    visited=[parent]
    while file:
        currentCell=file.pop(0)
        for child in currentCell.children_cells:
            if (child not in visited):
                visited.append(child)
                file.append(child)
    return visited





#Renvoie une lise contenant les predecesseurs de chaque celulle d'une liste de celulle donnée
def predecesorList(cellList):
    preds=[[] for _ in range(len(cellList))]
    for i in range(len(cellList)):
        for parent in cellList[i].parent_cells:
            if parent in cellList:
                preds[i].append(parent)
    return preds

#Supprime une celulle d'une liste de predecesseurs
def removePred(predList,cell):
    for cellList in predList:
        occurrence=cellList.count(cell)
        for _ in range(occurrence):
            cellList.remove(cell)

#Renvoie l'odre d'évaluation d'une liste de cellule
def evalOrder(cell):
    cellList=childrenCellsRec(cell)
    pred=predecesorList(cellList)
    order=[]
    while len(cellList)>0:
        i=0
        hasCycle=True
        while i<len(pred) and hasCycle==True:
            if len(pred[i])==0:
                hasCycle=False
                element=cellList.pop(i)
                order.append(element)
                pred.pop(i)
                removePred(pred,element)
            i+=1
        if hasCycle:
            raise Exception
    return order[1:]








