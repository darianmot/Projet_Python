""" Dans ce module, on s'occupe d'ordonner une liste de celulles à évaluer selon le tri topologique """

#Renvoie l'ensemble des cellules filles (récursive) d'une cellule
def childrenCellsRec(cell):
    l=[cell]
    for c in cell.children_cells:
       l.append(childrenCellsRec(c))
    return l

#Renvoie une lise contenant les predecesseurs de chaque celulle d'une liste de celulle donnée
def predecesorList(cellList):
    preds=[[] for _ in range(cellList)]
    for i in range(cellList):
        for parent in cellList[i].parent_cells:
            if parent in cellList:
                preds[i].append(parent)
    return preds

#Supprime une celulle d'une liste de predecesseurs
def removePred(predList,cell):
    for cellList in predList:
        ocurrence=cellList.count(cell)
        for _ in range(ocurrence):
            cellList.remove(cell)

def evalOrder(cell):
    cellList=childrenCellsRec(cell)
    pred=predecesorList(cellList)
    order=[]
    while len(cellList)>0:
        i=0
        hasCycle=True
        while i<len(cellList)or hasCycle==False:
            if len(pred[i])==0:
                hasCycle=False
                element=cellList.pop(i)
                order.append(element)
                pred.remove(i)
                removePred(pred,element)
            i+=1
        if hasCycle:
            return '#Error : circle cell depency'
    return order








