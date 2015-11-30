__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow, structures
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

app = mainwindow.QtWidgets.QApplication(sys.argv)
matrix=structures.network()
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow,matrix)

# ui.ask_coords.connect(traitement)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())




