__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow, structures,cells_traitements.functions as functions
import cells_traitements.decomposition as decomposition,recOrd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

network = structures.network()
knownFunctions=functions.Knownfunctions()
app = mainwindow.QtWidgets.QApplication(sys.argv)
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow,network)

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
            ui.return_value.emit(x, y, str(value))
            for ChildCell in cell.children_cells:                                  #On recalcul tous les neighbours de cell
                    traitement(ChildCell.x, ChildCell.y, ChildCell.input)
        else:
            cell.value = string
            if cell.input == "":                                                 #Si le input n'était pas définie, on le fait
                cell.input = string
                if len(cell.parent_cells) > 0:
                    for parentCell in cell.parent_cells: #On enleve cell comme neighbour eventuel
                        parentCell.removeChildCell(cell)
            elif cell.input[0] == '=':                                           #Si le input commençait par '=', on ne le change que son evaluation est different de ce que affiche la celulle
                if str(decomposition.evaluation(network, cell.input[1:], knownFunctions)) != cell.value:
                    cell.input = cell.value
                    if len(cell.parent_cells) > 0:
                        for parentCell in cell.parent_cells: #On enleve cell comme neighbour eventuel
                            parentCell.removeChildCell(cell)
            else:                                                              #Dans les autres cas, on change le input
                cell.input = string
                if len(cell.parent_cells) > 0:
                    for parentCell in cell.parent_cells: #On enleve cell comme neighbour eventuel
                        parentCell.removeChildCell(cell)
            for ChildCell in cell.children_cells:                                  #On recalcul tous les neighbours de cell
                    traitement(ChildCell.x, ChildCell.y, ChildCell.input)

    recOrd.binder2(network)
ui.read_value.connect(traitement)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


