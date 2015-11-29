import visu.columns_labels as columns_labels
class Cell (object): #caractéristiques et organisation d'une cellule

    def __init__(self,X,Y,value):
        self.X = X
        self.Y = Y
        self.value = value
        self.status = True
        self.name = str(columns_labels.generate(Y+1)[-1]) + str(X+1)     #chaine de caractères
        self.neighbours = []             #liste des cellules dépendant de celle-ci

