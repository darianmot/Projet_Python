__authors__ = "Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys, visu.mainwindow as mainwindow, visu.funwindow as funWindow, visu.addfunwindow as addfunwindow, visu.quitwin as quitWindow,  \
    graph as graphic
import structures, cells_traitements.functions as functions, record
import cells_traitements.tirette as tirette, cells_traitements.evaluation as evalutation
import pickle
from PyQt5 import QtWidgets, Qt

knownFunctions = pickle.load(open('knownFunctions.p', 'rb'))
knownFunctions.addCategory("Date et heure")
knownFunctions.addCategory("Texte")
knownFunctions.addCategory("Physique")
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
MainWindow = mainwindow.MyMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow, network)
record.etatXls(ui_mainwindow)

# Function Window
Funwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow, knownFunctions)
# graphwindow
graphwindow = QtWidgets.QDialog()
ui_graphwindow = graphic.Ui_MainWindowgraph()
ui_graphwindow.setupUi(graphwindow)
# AddFunction Window
AddFunwindow = QtWidgets.QDialog()
ui_addfunwindow = addfunwindow.Ui_Dialog()
ui_addfunwindow.setupUi(AddFunwindow, knownFunctions)
#Quit/Save window
Quitwindow= QtWidgets.QDialog()
ui_quitWindow = quitWindow.Ui_quitwin()
ui_quitWindow.setupUi(Quitwindow)

# processus de tirette (coin inférieur droit d'une case sélectionnée)

def expension_process(cells_selected):
    cells_selected = cells_selected[0]

    # application de l'extension de formule (tirette)
    tirette.formuleExpanse(cells_selected,network,ui_mainwindow)

    # efface les rectangles verts, fin de l'effet tirette
    tirette.endTirette(ui_mainwindow, cells_selected)



def functionAdded(name, descrition, evaluation, category):
    knownFunctions.addFun(functions.Function(name, evaluation, descrition, category))
    print('Ajout de la fonction {}'.format(name))
    pickle.dump(knownFunctions, open('knownFunctions.p', 'wb')) #Sauvegarde de l'ajout pour la prochaine ouverture
    ui_funWinfow.retranslateUi(Funwindow, knownFunctions)


def windowopen():  # to open the window open....
    try:
        extension = "(*.p *.xls *.csv)" if record.HASXLRD else "(*.p *.csv)"
        fileWindow = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Ouvrir', '', extension)
        address = fileWindow[0]
        record.extensionreader(address, ui_mainwindow, network)
    except IndexError:
        print("No file selected")


def windowsave():  # to open the window save....
    fileWindow = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Enregistrer', '', "(*.p)")
    address = fileWindow[0]  # faut mettre l'extension du format genre fichier.pyc ou fichier.xls dans la barre de saisie
    name=record.fileName(address)
    record.writter_marshalling(network,name,ui_mainwindow)


def export():
    extension = "(*.xls *.csv)" if record.HASXLWT else "(*.csv)"
    fileWindow = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Enregistrer', '', extension)
    address = fileWindow[0]
    record.extensionwritter(address, network, ui_mainwindow)



# Renitialise la feuille de calcul
def reset_table():
    ui_mainwindow.tableWidget.resetTable()
    network.reset(ui_mainwindow.tableWidget.initialRowsNumber, ui_mainwindow.tableWidget.initialColumnsNumber)
    ui_mainwindow.lineEdit.clear()
    ui_mainwindow.tableWidget.setFocus()
    ui_mainwindow.indicator.setText("Nouvelle Feuille")
    ui_mainwindow.tableWidget.network.saved = False



  #Quit

def quit_enacell():
    if ui_mainwindow.tableWidget.network.saved:
        MainWindow.close()
    else:
        Quitwindow.show()

def force_quit():
    ui_mainwindow.tableWidget.network.saved = True
    Quitwindow.close()
    quit_enacell()


ui_quitWindow.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(windowsave)
ui_quitWindow.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(Quitwindow.close)
ui_quitWindow.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(force_quit)

    #Connexion des boutons de l'interface
    #Menus
ui_mainwindow.actionenregistrer.triggered.connect(windowsave)
ui_mainwindow.menu_enregistrer.triggered.connect(windowsave)
ui_mainwindow.actionExport.triggered.connect(export)
ui_mainwindow.actionOuvrir.triggered.connect(windowopen)
ui_mainwindow.menu_ouvrir.triggered.connect(windowopen)
ui_mainwindow.menu_quit.triggered.connect(quit_enacell)
ui_mainwindow.new_button.triggered.connect(reset_table)
MainWindow.asked_quit.connect(Quitwindow.show)


    #Table
ui_mainwindow.tableWidget.read_input.connect(lambda x, y, string : evalutation.cellEvaluation(x, y, string, network, ui_mainwindow, knownFunctions))
ui_mainwindow.tableWidget.filter.cellExpended.connect(expension_process)

    #Function windows
ui_funWinfow.toolAdd.released.connect(AddFunwindow.show)
ui_mainwindow.functionButton.released.connect(Funwindow.show)
ui_addfunwindow.sendFunData.connect(functionAdded)


    #Graphs
ui_mainwindow.graph.triggered.connect(graphwindow.show)
def draw_graph(current_row):
    graphic.graph_selector(current_row,ui_mainwindow,MainWindow.statusBar,network,ui_graphwindow)






ui_graphwindow.okSignal.connect(draw_graph)
MainWindow.showMaximized()
splash.finish(MainWindow)
sys.exit(app.exec_())
