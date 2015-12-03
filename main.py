__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow, structures
import cells_traitements.decomposition as decomposition
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

network = structures.network()

app = mainwindow.QtWidgets.QApplication(sys.argv)
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow,network)

def traitement(x, y, string):
    if string[0] == '=':
        value = decomposition.evaluation(network,string[1:])
        network.matrix[x][y].value = str(value)
        network.matrix[x][y].input = string
        ui.return_value.emit(x ,y, str(value))
    else:
        network.matrix[x][y].value = string

ui.read_value.connect(traitement)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


