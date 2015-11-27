# ATTENTION : vu qu'on a modifié ce fichier, mainwindow.ui est devenu obsolète
from PyQt5 import QtCore, QtGui, QtWidgets
import columns_labels
CELLWIDTH=100
CELLHEIGHT=30



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Initialisation
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")

        #On ajuste le nombre de colonnes/lignes en fonction de la taille de l'écran
        screen = QtWidgets.QDesktopWidget()
        initalRowsNumber=int(2*screen.height()/CELLHEIGHT)
        initalColunmsNumber=int(2*screen.width()/CELLWIDTH)
        self.tableWidget.setColumnCount(initalColunmsNumber)
        self.tableWidget.setRowCount(initalRowsNumber)

        #On attribue un identifiant à chaques colonnes
        for k in range(initalRowsNumber):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(k,item)

        #On attribue un identifiant à chaques lignes
        for k in range(initalColunmsNumber):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(k, item)

        #La toolbox et le menu
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuSsmenu1 = QtWidgets.QMenu(self.menuFichier)
        self.menuSsmenu1.setObjectName("menuSsmenu1")
        self.menuSsmenu2 = QtWidgets.QMenu(self.menuFichier)
        self.menuSsmenu2.setObjectName("menuSsmenu2")
        MainWindow.setMenuBar(self.menubar)
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("stremio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOuvrir.setIcon(icon)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionAction1 = QtWidgets.QAction(MainWindow)
        self.actionAction1.setObjectName("actionAction1")
        self.actionAction2 = QtWidgets.QAction(MainWindow)
        self.actionAction2.setObjectName("actionAction2")
        self.actionAction2_1 = QtWidgets.QAction(MainWindow)
        self.actionAction2_1.setObjectName("actionAction2_1")
        self.toolBar.addAction(self.actionOuvrir)
        self.toolBar.addSeparator()
        self.menuSsmenu1.addAction(self.actionAction1)
        self.menuSsmenu1.addAction(self.actionAction2)
        self.menuSsmenu2.addAction(self.actionAction2_1)
        self.menuFichier.addAction(self.menuSsmenu1.menuAction())
        self.menuFichier.addAction(self.menuSsmenu2.menuAction())
        self.menubar.addAction(self.menuFichier.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        screen = QtWidgets.QDesktopWidget()
        initalRowsNumber=int(2*screen.height()/CELLHEIGHT)
        initalColunmsNumber=int(2*screen.width()/CELLWIDTH)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        columnsLabels=columns_labels.generate(self.tableWidget.columnCount()) #generattion de la liste des labels
        
        #On renomme chaques lignes
        for k in range(1,self.tableWidget.rowCount()+1):
            item=self.tableWidget.verticalHeaderItem(k-1)
            item.setText(_translate("MainWindow",str(k)))

        #On renomme chaques colonnes
        for k in range(1,self.tableWidget.columnCount()+1):
            item = self.tableWidget.horizontalHeaderItem(k-1)
            item.setText(_translate("MainWindow", columnsLabels[k-1]))

        #On ajoute des lignes à la fin si la bar VERTICALE de scrolling est en bas
        verticalscrollbar=self.tableWidget.verticalScrollBar()
        def ajoutRows():
            if verticalscrollbar.value()==verticalscrollbar.maximum():
                for _ in range(initalRowsNumber//3):
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
        verticalscrollbar.valueChanged.connect(ajoutRows)

        #On ajoute des colonnes à la fin si la bar HORIZONTALE de scrolling est en bas (il faut cette fois renommer les colonnes)
        horizontalscrollbar=self.tableWidget.horizontalScrollBar()
        def ajoutColumns():
            if horizontalscrollbar.value()==horizontalscrollbar.maximum():
                for _ in range(initalColunmsNumber//3):
                    self.tableWidget.insertColumn(self.tableWidget.columnCount())
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(self.tableWidget.columnCount()-1, item)
                    item = self.tableWidget.horizontalHeaderItem(self.tableWidget.columnCount()-1)
                    columns_labels.add(columnsLabels,1)
                    item.setText(_translate("MainWindow", columnsLabels[self.tableWidget.columnCount()-1]))
        horizontalscrollbar.valueChanged.connect(ajoutColumns)

        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuFichier.setTitle(_translate("MainWindow", "Menu1"))
        self.menuSsmenu1.setTitle(_translate("MainWindow", "ssmenu1"))
        self.menuSsmenu2.setTitle(_translate("MainWindow", "ssmenu2"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionOuvrir.setToolTip(_translate("MainWindow", "infobulle"))
        self.actionAction1.setText(_translate("MainWindow", "action1"))
        self.actionAction2.setText(_translate("MainWindow", "action2"))
        self.actionAction2_1.setText(_translate("MainWindow", "action21"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized() #Pour agrandir au max la fenetre
    sys.exit(app.exec_())


