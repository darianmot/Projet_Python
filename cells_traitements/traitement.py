import structures





def reconnaisssance(a,b):
    print(a,b)

#Retourne le nouveau contenu de la case en chaine de caractère
def value(a):
    print(a.text())


active_cells=[]   #liste des cellules actives


#le traitement appliqué à la chaine de carateres obtenue:
def traitement(x, y, string):
    if string[0] == '=':
        for cell in active_cells:
            if cell.name in string:
                str(cell.value).join(string.split(cell.name))     #remplace le nom d'une cellule par sa valeur
        v = str(eval(string[1:]))
        active_cells.append(structures.Cell(x,y,v))
        main.ui.return_value.emit(x,y,v)
    else:
        active_cells.append(structures.Cell(x,y,string))



