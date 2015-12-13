__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow,visu.funwindow as funWindow, structures,cells_traitements.functions as functions
import cells_traitements.decomposition as decomposition,recOrd,cells_traitements.tritopologique as tritopologique
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
    print('Evaluation de {}...'.format(cell.name),end='')
    if len(string) > 0:
        if string[0] == '=':
            value = decomposition.evaluation(network,string[1:], knownFunctions)
            cell.parent_cells = decomposition.parentCells(network, string[1:])
            for parentCell in cell.parent_cells:
                parentCell.addChildCell(cell)
            cell.value = str(value)
            cell.input = string
            ui_mainwindow.tableWidget.return_value.emit(x, y, str(cell.value))
        else:
            cell.value = string
            cell.input = string
            ui_mainwindow.tableWidget.return_value.emit(x, y, str(cell.value))
        print(' Done')
        try:
            order=tritopologique.evalOrder(cell)
            for child in order:
                child.value=str(decomposition.evaluation(network,child.input[1:],knownFunctions))
                ui_mainwindow.tableWidget.return_value.emit(child.x,child.y,child.value)
        except Exception:
            ui_mainwindow.tableWidget.return_value.emit(x, y, '#Error : Circle dependancy')
    recOrd.binder2(network)

ui_mainwindow.tableWidget.read_value.connect(traitement)
ui_mainwindow.functionButton.released.connect(Funwindow.show)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


