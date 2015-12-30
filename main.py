__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow,visu.funwindow as funWindow, visu.addfunwindow as addfunwindow,graph as graphic
import structures,cells_traitements.functions as functions,recOrd
import cells_traitements.decomposition as decomposition,cells_traitements.tritopologique as tritopologique
import time,pickle
from PyQt5 import QtWidgets,Qt, QtGui


knownFunctions=pickle.load(open('knownFunctions.p','rb'))
app = mainwindow.QtWidgets.QApplication(sys.argv)

#Main Window
network = structures.network()
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow,network)

#Function Window
Funwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow,knownFunctions)
#graphwindow
graphwindow=QtWidgets.QMainWindow()
ui_graphwindow = graphic.Ui_MainWindowgraph()
ui_graphwindow.setupUi((graphwindow))
#AddFunction Window
AddFunwindow = QtWidgets.QDialog()
ui_addfunwindow = addfunwindow.Ui_Dialog()
ui_addfunwindow.setupUi(AddFunwindow,knownFunctions)



# Traitement des cellules (peut être faudrait il trouver moyen de bouger ça dans un module)

def traitement(x, y, string):
    cell = network.getCell(x, y)
    cell.input=string
    oldValue=cell.value
    t_init=time.time()
    if len(string) > 0:
        print('Evaluation de {0} et de ses cellules filles ... '.format(cell.name,len(cell.children_cells)),end='')
        try:
            if string[0] == '=':
                cell.parent_cells = decomposition.parentCells(network, string[1:])
                for parentCell in cell.parent_cells:
                    parentCell.addChildCell(cell)
            newValue=str(decomposition.evaluation(network,string[1:], knownFunctions)) if string[0]=='=' else string
            if oldValue!=newValue:
                if string[0] == '=':
                    cell.value = newValue
                else:
                    cell.value = string
                ui_mainwindow.tableWidget.return_value.emit(x, y, str(cell.value))
                try:
                    order=tritopologique.evalOrder(cell)
                    for child in order:
                        child.value=str(decomposition.evaluation(network,child.input[1:],knownFunctions))
                        ui_mainwindow.tableWidget.return_value.emit(child.x,child.y,child.value)
                except decomposition.Error as e:
                    ui_mainwindow.tableWidget.return_value.emit(x, y, e.disp)
        except decomposition.Error as e:
            ui_mainwindow.tableWidget.return_value.emit(x, y, e.disp)
        t_end=time.time()
        print('Done : {}s'.format(t_end-t_init))



#processus de tirette (coin inférieur droit d'une case sélectionnée)

def expension_process(cells_selected):

    cells_selected=cells_selected[0]
    print("nombre de colonnes:", cells_selected.columnCount())
    print("nombre de lignes:", cells_selected.rowCount())
    print("première ligne:", cells_selected.topRow())
    print("dernière ligne:", cells_selected.bottomRow())
    print("colonne de gauche:", cells_selected.leftColumn())
    print("colonne de droite:", cells_selected.rightColumn())

    # application de l'extension de formule (tirette)

    if cells_selected.leftColumn()==cells_selected.rightColumn():
        column=cells_selected.rightColumn()
        r0=cells_selected.topRow() #Ligne initiale
        input=network.getCell(r0,column).input
        if len(input)==0:
            pass
        elif input[0]!='=':
            for i in range(r0+1,cells_selected.bottomRow()+1):
                if ui_mainwindow.tableWidget.item(i,column)==None:
                    ui_mainwindow.tableWidget.setItem(i,column,QtWidgets.QTableWidgetItem())
                traitement(i,column,input)
        else:
            decomposition0=decomposition.decompo(input)
            for i in range(r0+1,cells_selected.bottomRow()+1):
                rows=i-r0
                newinput=decomposition.verticalPull(decomposition0,rows)
                if ui_mainwindow.tableWidget.item(i,column)==None:
                    ui_mainwindow.tableWidget.setItem(i,column,QtWidgets.QTableWidgetItem())
                traitement(i,column,newinput)
    elif cells_selected.topRow()==cells_selected.bottomRow():
        row=cells_selected.bottomRow()
        c0=cells_selected.leftColumn() #Colonne intiale
        input=network.getCell(row,c0).input
        if len(input)==0:
            pass
        elif input[0]!='=':
            for i in range(c0+1,cells_selected.rightColumn()+1):
                if ui_mainwindow.tableWidget.item(row,i)==None:
                    ui_mainwindow.tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem())
                traitement(row,i,input)
        else:
            decomposition0=decomposition.decompo(input)
            for i in range(c0+1,cells_selected.rightColumn()+1):
                columns=i-c0
                newinput=decomposition.horizontalPull(decomposition0,columns,ui_mainwindow.tableWidget.columnsLabels)
                if ui_mainwindow.tableWidget.item(row,i)==None:
                    ui_mainwindow.tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem())
                traitement(row,i,newinput)




    #efface les rectangles verts, fin de l'effet tirette
    width = ui_mainwindow.tableWidget.columnWidth(ui_mainwindow.tableWidget.currentColumn())
    height = ui_mainwindow.tableWidget.rowHeight(ui_mainwindow.tableWidget.currentRow())
    x = cells_selected.leftColumn() * width
    y = cells_selected.topRow() * height
    range_width = cells_selected.rightColumn() - cells_selected.leftColumn()+1
    range_height = cells_selected.bottomRow() - cells_selected.topRow()+1
    reset_rect = Qt.QRect()
    reset_rect.setRect(x,y,range_width * width,range_height* height)
    ui_mainwindow.tableWidget.viewport().repaint(reset_rect)



def functionAdded(name,descrition,evaluation,category):
    knownFunctions.addFun(functions.Function(name,evaluation,descrition,category))
    print('Ajout de la fonction {}'.format(name) )
    pickle.dump(knownFunctions,open('knownFunctions.p','wb'))
    ui_funWinfow.retranslateUi(Funwindow,knownFunctions)

def windowopen():#to open the window open....
    try:
        a=QtWidgets.QFileDialog.getOpenFileName(MainWindow,'Ouvrir','',"(*.pyc *xls *csv)")
        adress=a[0]
        recOrd.extensionreader(adress,ui_mainwindow,traitement)
    except IndexError:
        print("No file selected")

def windowsave():                      #to open the window save....
    a=QtWidgets.QFileDialog.getSaveFileName(MainWindow,'Enregistrer','',"(*.pyc *.xls *.csv)")
    adress=a[0]                                   #faut mettre l'extension du format genre fichier.pyc ou fichier.xls dans la barre de saisie
    recOrd.extensionwritter(adress,network)

# destinée à réinitialiser la feuille de calcul (pour nouvelle feuille) en cours de construction
def reset_table():
    global  ui_mainwindow
    global  network
    global  MainWindow
    ui_mainwindow.tableWidget.close()
    network = structures.network()
    ui_mainwindow.setTable(network)
    ui_mainwindow.verticalLayout.addWidget(ui_mainwindow.tableWidget)


# connexion des boutons de l'interface
ui_mainwindow.tableWidget.read_value.connect(traitement)
ui_mainwindow.tableWidget.filter.cellExpended.connect(expension_process)

ui_mainwindow.functionButton.released.connect(Funwindow.show)

ui_mainwindow.actionOuvrir.triggered.connect(windowopen)
ui_mainwindow.menu_ouvrir.triggered.connect(windowopen)

ui_mainwindow.actionenregistrer.triggered.connect(windowsave)
ui_mainwindow.menu_enregistrer.triggered.connect(windowsave)
ui_mainwindow.graph.triggered.connect(graphwindow.show)

ui_funWinfow.toolAdd.released.connect(AddFunwindow.show)
ui_addfunwindow.sendFunData.connect(functionAdded)

MainWindow.showMaximized() #Pour agrandir au max la fenetre

ui_mainwindow.menu_quit.triggered.connect(MainWindow.close)
ui_mainwindow.new_button.triggered.connect(reset_table)

sys.exit(app.exec_())