__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow,visu.funwindow as funWindow, structures,cells_traitements.functions as functions
import cells_traitements.decomposition as decomposition,recOrd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

network = structures.network()
knownFunctions=functions.Knownfunctions()
app = mainwindow.QtWidgets.QApplication(sys.argv)

MainWindow = mainwindow.QtWidgets.QMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow,network)

Funwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow,knownFunctions)


def traitement(x, y, string):
    cell = network.getCell(x, y)
    if len(string) > 0:
        if string[0] == '=':

            value = decomposition.evaluation(network,string[1:], knownFunctions)
            cell.parent_cells = decomposition.parentCells(network, string[1:])
            for parentCell in cell.parent_cells: #On ajoute cell comme neighbour eventuel
                parentCell.addChildCell(cell)
            cell.value = str(value)
            cell.input = string
            ui_mainwindow.return_value.emit(x, y, str(value))
            for ChildCell in cell.children_cells:                                  #On recalcul tous les neighbours de cell
                    traitement(ChildCell.x, ChildCell.y, ChildCell.input)
        else:
            cell.value = string
            if cell.input == "":                                                 #Si le input n'était pas définie, on le fait
                cell.input = string
            elif cell.input[0] == '=':                                           #Si le input commençait par '=', on ne le change que son evaluation est different de ce que affiche la celulle
                if str(decomposition.evaluation(network, cell.input[1:], knownFunctions)) != cell.value:
                    cell.input = cell.value
            else:                                                              #Dans les autres cas, on change le input
                cell.input = string
            # if len(cell.parent_cells) > 0:
            #         for parentCell in cell.parent_cells: #On enleve cell comme neighbour eventuel
            #             parentCell.removeChildCell(cell)
            for ChildCell in cell.children_cells:                                  #On recalcul tous les neighbours de cell
                    traitement(ChildCell.x, ChildCell.y, ChildCell.input)
    recOrd.binder2(network)


ui_mainwindow.read_value.connect(traitement)
ui_mainwindow.functionButton.released.connect(Funwindow.show)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


