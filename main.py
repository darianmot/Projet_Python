__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow,visu.funwindow as funWindow, visu.registerwindow as registerwindow, visu.addfunwindow as addfunwindow
import structures,cells_traitements.functions as functions
import cells_traitements.decomposition as decomposition,recOrd,cells_traitements.tritopologique as tritopologique
import time
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

network = structures.network()
knownFunctions=functions.Knownfunctions()
app = mainwindow.QtWidgets.QApplication(sys.argv)

#Main Window
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow,network)

#Function Window
Funwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow,knownFunctions)

#Open Window
# Registerwindow = QtWidgets.QDialog()
# ui_registerwindow = registerwindow.ui_MainWindow()
# ui_registerwindow.setupUi(Registerwindow)

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
        try:
            newValue=str(decomposition.evaluation(network,string[1:], knownFunctions)) if string[0]=='=' else string
        except decomposition.Error as e:
            newValue=e.disp
        if oldValue!=newValue:
            print('Evaluation de {0} et de ses cellules filles ... '.format(cell.name,len(cell.children_cells)),end='')
            if string[0] == '=':
                cell.parent_cells = decomposition.parentCells(network, string[1:])
                for parentCell in cell.parent_cells:
                    parentCell.addChildCell(cell)
                cell.value = newValue
                ui_mainwindow.tableWidget.return_value.emit(x, y, str(cell.value))
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
            t_end=time.time()
            print('Done : {}s'.format(t_end-t_init))

    recOrd.writter_xls(network)

def reader_xls(file):
    import xlrd
    #opening of the file as a binder
    binder=xlrd.open_workbook(file)
    #listing of sheet names
    sheets=binder.sheet_names()
    #recovering of the i eme sheet
    sheet=binder.sheet_by_name(sheets[0])
    #display the sheet but where find it
    from main import ui_mainwindow, traitement
    for i in range(1,sheet.nrows):
        for j in range(1,sheet.ncols):
         content=sheet.cell_value(i,j)
         item= QtWidgets.QTableWidgetItem()
         ui_mainwindow.tableWidget.setItem(i,j,item)
         traitement(i,j,content)
#a=input('ecrire test.xls')
#recOrd.reader_xls(a)
def functionAdded(name,descrition,evaluation,category):
    knownFunctions.addFun(functions.Function(name,evaluation,descrition,category))
    ui_funWinfow.retranslateUi(Funwindow,knownFunctions)

ui_mainwindow.tableWidget.read_value.connect(traitement)
ui_mainwindow.functionButton.released.connect(Funwindow.show)
# ui_mainwindow.actionOuvrir.triggered.connect(Registerwindow.show)
ui_funWinfow.toolAdd.released.connect(AddFunwindow.show)
ui_addfunwindow.sendFunData.connect(functionAdded)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


