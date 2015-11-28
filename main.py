__authors__="Darian MOTAMED, Hugo CHOULY, Atime RONDA,Anas DARWICH"
import sys,visu.mainwindow as mainwindow, cells_traitements.traitement as traitement
from PyQt5 import QtCore, QtGui, QtWidgets


app = mainwindow.QtWidgets.QApplication(sys.argv)
MainWindow = mainwindow.QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow)

ui.ask_coords.connect(traitement.reconnaisssance)

MainWindow.showMaximized() #Pour agrandir au max la fenetre
sys.exit(app.exec_())




