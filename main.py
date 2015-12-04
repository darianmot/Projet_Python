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
    cell=network.getCell(x,y)
    if string[0] == '=':
        value = decomposition.evaluation(network,string[1:])
        for parentCell in decomposition.parentCells(network,string[1:]): #On ajoute cell comme neighbour
            parentCell.addNeighbour(cell)
        cell.value = str(value)
        cell.input = string
        ui.return_value.emit(x ,y, str(value))
        for neighbour in cell.neighbours:                                  #On recalcul tous les neighbours de cell
            traitement(neighbour.x,neighbour.y,neighbour.input)
    else:
        cell.value = string
        for neighbour in cell.neighbours:
            traitement(neighbour.x,neighbour.y,neighbour.input)


ui.read_value.connect(traitement)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


