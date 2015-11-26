# ATTENTION : vu qu'on a modifié ce fichier, mainwindow.ui est devenu obsolète
from PyQt5 import QtCore, QtGui, QtWidgets
import columns_labels
CELLWIDTH=100
CELLHEIGHT=30



class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        screen = QtWidgets.QDesktopWidget()
        verticalCellNumber=int(2*screen.height()/CELLHEIGHT)
        horizontalCellNumber=int(2*screen.width()/CELLWIDTH)

        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setColumnCount(horizontalCellNumber)

        self.tableWidget.setRowCount(verticalCellNumber)

        for k in range(verticalCellNumber):                         #On attribue un identifiant à chaques colonnes
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(k,item)

        for k in range(horizontalCellNumber):                       #On attribue un identifiant à chaques lignes
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(k, item)

        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        #Le menu
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
        verticalCellNumber=int(2*screen.height()/CELLHEIGHT)
        horizontalCellNumber=int(2*screen.width()/CELLWIDTH)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        columnsLabels=columns_labels.generate(horizontalCellNumber)

        for k in range(1,self.tableWidget.rowCount()+1):            #On renomme chaques colonnes
            item=self.tableWidget.verticalHeaderItem(k-1)
            item.setText(_translate("MainWindow",str(k)))

        for k in range(1,self.tableWidget.columnCount()+1):         #On renomme chaques lignes
            item = self.tableWidget.horizontalHeaderItem(k-1)
            item.setText(_translate("MainWindow", columnsLabels[k-1]))

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


