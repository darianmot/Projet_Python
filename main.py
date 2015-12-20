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

MainWindow = mainwindow.QtWidgets.QMainWindow()
ui_mainwindow = mainwindow.Ui_MainWindow()
ui_mainwindow.setupUi(MainWindow,network)



Funwindow = QtWidgets.QDialog()
#Registerwindow = QtWidgets.QFileDialog.getOpenFileName()
AddFunwindow = QtWidgets.QDialog()
ui_funWinfow = funWindow.Ui_funwindow()
ui_funWinfow.setupUi(Funwindow,knownFunctions)
#ui_registerwindow = registerwindow.UI_MainWindow()
#ui_registerwindow.setupUi(Registerwindow)
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

    recOrd.writter_csv(network)




def reader_csv(file):

    sheet=csv.reader(open(file))
    i=0
    j=0
    for row in sheet :
        i+=1
        for j  in range(0,len(row)):
            j+=1
            item= QtWidgets.QTableWidgetItem()
            ui_mainwindow.tableWidget.setItem(i,j,item)
            content=row[j-1]
            traitement(i,j,content)


a=input('écrit newfile.csv')
reader_csv(a)
def functionAdded(name,descrition,evaluation,category):
    knownFunctions.addFun(functions.Function(name,evaluation,descrition,category))
    ui_funWinfow.retranslateUi(Funwindow,knownFunctions)

ui_mainwindow.tableWidget.read_value.connect(traitement)
ui_mainwindow.functionButton.released.connect(Funwindow.show)
ui_mainwindow.actionOuvrir.triggered.connect(QtWidgets.QFileDialog.getOpenFileName)
ui_funWinfow.toolAdd.released.connect(AddFunwindow.show)
ui_addfunwindow.sendFunData.connect(functionAdded)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())


