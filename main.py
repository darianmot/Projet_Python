__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow, structures
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

active_cells=[]   #liste des cellules actives


#le traitement appliqué à la chaine de carateres obtenue:
def traitement(x, y, string):
    if string[0] == '=':
        for cell in active_cells:
            if str(cell.name) in string:
                string = str(cell.value).join(string.split(cell.name))     #remplace le nom d'une cellule par sa valeur
        v = str(eval(string[1:]))
        active_cells.append(structures.Cell(x,y,v))
        ui.return_value.emit(x,y,v)



app = mainwindow.QtWidgets.QApplication(sys.argv)
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow)

ui.ask_coords.connect(traitement)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())




