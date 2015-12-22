import matplotlib.pyplot as plt
def graph(listeValue,ordonnée,abscisse,title,xmin,xmax,ymin,ymax,color):
    newliste=[x.value for x in listeValue]
    plt.plot[newliste,color]
    plt.ylabel(ordonnée)
    plt.xlabel(abscisse)
    plt.title(title)
    plt.axis(xmin,xmax,ymin,ymax)
    plt.show()



