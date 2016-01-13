__authors__ = "Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys, visu.mainwindow as mainwindow, visu.funwindow as funWindow, visu.addfunwindow as addfunwindow, \
    graph as graphic
import structures, cells_traitements.functions as functions, recOrd
import cells_traitements.tirette as tirette, cells_traitements.evaluation as evalutation
import pickle
from PyQt5 import QtWidgets, Qt, QtCore

knownFunctions = pickle.load(open('knownFunctions.p', 'rb'))
app = mainwindow.QtWidgets.QApplication(sys.argv)

pixmap = Qt.QPixmap("visu/icons/Logo_ENAC.png")
splash = Qt.QSplashScreen(pixmap)
splash.show()
splash.raise_()
splash.repaint()
splash.showMessage("Chargement")
app.processEvents()


# Main Window
network = structures.network()
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow, network)
recOrd.etatXls(ui_mainwindow)

# Function Window
Funwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow, knownFunctions)
# graphwindow
graphwindow = QtWidgets.QMainWindow()
ui_graphwindow = graphic.Ui_MainWindowgraph()
ui_graphwindow.setupUi((graphwindow))
# AddFunction Window
AddFunwindow = QtWidgets.QDialog()
ui_addfunwindow = addfunwindow.Ui_Dialog()
ui_addfunwindow.setupUi(AddFunwindow, knownFunctions)

# processus de tirette (coin inférieur droit d'une case sélectionnée)

def expension_process(cells_selected):
    cells_selected = cells_selected[0]

    # application de l'extension de formule (tirette)
    tirette.formuleExpanse(cells_selected,network,ui_mainwindow)

    # efface les rectangles verts, fin de l'effet tirette
    width = ui_mainwindow.tableWidget.columnWidth(ui_mainwindow.tableWidget.currentColumn())
    height = ui_mainwindow.tableWidget.rowHeight(ui_mainwindow.tableWidget.currentRow())
    x = cells_selected.leftColumn() * width
    y = cells_selected.topRow() * height
    range_width = cells_selected.rightColumn() - cells_selected.leftColumn() + 1
    range_height = cells_selected.bottomRow() - cells_selected.topRow() + 1
    reset_rect = Qt.QRect()
    reset_rect.setRect(x, y, range_width * width, range_height * height)
    ui_mainwindow.tableWidget.viewport().repaint(reset_rect)


def functionAdded(name, descrition, evaluation, category):
    knownFunctions.addFun(functions.Function(name, evaluation, descrition, category))
    print('Ajout de la fonction {}'.format(name))
    pickle.dump(knownFunctions, open('knownFunctions.p', 'wb')) #Sauvegarde de l'ajout pour la prochaine ouverture
    ui_funWinfow.retranslateUi(Funwindow, knownFunctions)


def windowopen():  # to open the window open....
    try:
        extension = "(*.p *.xls *.csv)" if recOrd.HASXLRD else "(*.p *.csv)"
        fileWindow = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Ouvrir', '', extension)
        address = fileWindow[0]
        recOrd.extensionreader(address, ui_mainwindow, network)
    except IndexError:
        print("No file selected")


def windowsave():  # to open the window save....
    fileWindow = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Enregistrer', '', "(*.p)")
    address = fileWindow[0]  # faut mettre l'extension du format genre fichier.pyc ou fichier.xls dans la barre de saisie
    name=recOrd.fileName(address)
    recOrd.writter_marshalling(network,name)
    ui_mainwindow.indicator.setText('Sauvegardé')

def export():
    extension = "(*.xls *.csv)" if recOrd.HASXLWT else "(*.p *.csv)"
    fileWindow = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Enregistrer', '', extension)
    address = fileWindow[0]
    recOrd.extensionwritter(address, network, ui_mainwindow)


# destinée à réinitialiser la feuille de calcul (pour nouvelle feuille) en cours de construction
def reset_table():
    ui_mainwindow.tableWidget.resetTable()
    network.reset(ui_mainwindow.tableWidget.initialRowsNumber, ui_mainwindow.tableWidget.initialColumnsNumber)
    ui_mainwindow.lineEdit.clear()
    ui_mainwindow.tableWidget.setFocus()
    ui_mainwindow.indicator.setText("Nouvelle Feuille")



#Partie Graphique

def graphiques():
    ui_mainwindow.indicator.setText("Sélectionnez une ligne ou colonne et appuyez sur Valider")
    btn = QtWidgets.QPushButton("Valider")
    btn.clicked.connect(lambda : action1(btn))
    MainWindow.statusBar().addWidget(btn)

def action1(btn):
    ui_mainwindow.lineEdit.blockSignals(True) #Pour éviter les interactions de la lineEdit pendant la selection
    L1=[]
    for item in ui_mainwindow.tableWidget.selectedItems():
        L1.append(network.getCell(item.row(), item.column()))
    b = True
    for i in range(1, len(L1)):
        if L1[0].x == L1[i].x or L1[0].y == L1[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            b = False
            break
    if b:
        print(L1)
        ui_mainwindow.indicator.setText("Sélectionnez une nouvelle ligne ou colonne et appuyez sur Valider")
        MainWindow.statusBar().removeWidget(btn)
        btn2 = QtWidgets.QPushButton("Valider")
        btn2.clicked.connect(lambda : action2(btn2, L1))
        MainWindow.statusBar().addWidget(btn2)
    MainWindow.statusBar().removeWidget(btn)

def action2(btn2, L1):
    L2=[]
    for item in ui_mainwindow.tableWidget.selectedItems():
        L2.append(network.getCell(item.row(), item.column()))
    b = True
    for i in range(1, len(L2)):
        if L2[0].x == L2[i].x or L2[0].y == L2[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou une seule colonne")
            b = False
            break
    if b:
        print(L1, L2)
        if len(L1) == len(L2):
            graphic.mainGraphFunction(L1, L2, A=0)
            ui_mainwindow.indicator.setText("La sélection est correcte")
            add(L1,L2)

        else:
            ui_mainwindow.indicator.setText("Erreur: Sélections de tailles différentes")
    MainWindow.statusBar().removeWidget(btn2)
    ui_mainwindow.lineEdit.setText(network.getCell(ui_mainwindow.tableWidget.currentRow(),ui_mainwindow.tableWidget.currentColumn()).input)
    ui_mainwindow.lineEdit.blockSignals(False)

def add(L1,L2):

    ui_mainwindow.indicator.setText("voulez vous superposer une autre courbe?")
    btn_add=QtWidgets.QPushButton("+add")
    MainWindow.statusBar().addWidget(btn_add)
    btn_cancel=QtWidgets.QPushButton("annuler")
    MainWindow.statusBar().addWidget(btn_cancel)
    def add_2():
        MainWindow.statusBar().removeWidget(btn_add)
        MainWindow.statusBar().removeWidget(btn_cancel)
        graphiques()
        graphic.close_graph()

    def cancel():
        MainWindow.statusBar().removeWidget(btn_add)
        MainWindow.statusBar().removeWidget(btn_cancel)
        ui_mainwindow.indicator.setText("")
    btn_add.clicked.connect(add_2)
    btn_cancel.clicked.connect(cancel)



    #Connexion des boutons de l'interface
    #Menus
ui_mainwindow.actionenregistrer.triggered.connect(windowsave)
ui_mainwindow.menu_enregistrer.triggered.connect(windowsave)
ui_mainwindow.actionExport.triggered.connect(export)
ui_mainwindow.actionOuvrir.triggered.connect(windowopen)
ui_mainwindow.menu_ouvrir.triggered.connect(windowopen)
ui_mainwindow.menu_quit.triggered.connect(MainWindow.close)
ui_mainwindow.new_button.triggered.connect(reset_table)

    #Table
ui_mainwindow.tableWidget.read_input.connect(lambda x, y, string : evalutation.cellEvaluation(x, y, string, network, ui_mainwindow, knownFunctions))
ui_mainwindow.tableWidget.filter.cellExpended.connect(expension_process)

    #Function windows
ui_funWinfow.toolAdd.released.connect(AddFunwindow.show)
ui_mainwindow.functionButton.released.connect(Funwindow.show)
ui_addfunwindow.sendFunData.connect(functionAdded)

    #Graphs
ui_mainwindow.graph.triggered.connect(graphwindow.show)
ui_graphwindow.buttonBox.accepted.connect(graphiques)



MainWindow.showMaximized()
splash.finish(MainWindow)
sys.exit(app.exec_())
