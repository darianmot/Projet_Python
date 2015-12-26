__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow,visu.funwindow as funWindow, visu.addfunwindow as addfunwindow,graph as graphic
import structures,cells_traitements.functions as functions,recOrd
import cells_traitements.decomposition as decomposition,cells_traitements.tritopologique as tritopologique
import time,pickle
from PyQt5 import QtWidgets

network = structures.network()
knownFunctions=pickle.load(open('knownFunctions.p','rb'))
app = mainwindow.QtWidgets.QApplication(sys.argv)

#Main Window
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


def expension_process(cells_selected):

    cells_selected=cells_selected[0]
    #print("nombre de colonnes:", cells_selected.columnCount())
    #print("nombre de lignes:", cells_selected.rowCount())
    print("première ligne:", cells_selected.topRow())
    print("dernière ligne:", cells_selected.bottomRow())
    print("colonne de gauche:", cells_selected.leftColumn())
    print("colonne de droite:", cells_selected.rightColumn())
    graphic.cell(cells_selected,network)

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

sys.exit(app.exec_())