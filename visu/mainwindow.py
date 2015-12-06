# ATTENTION : vu qu'on a modifié ce fichier, mainwindow.ui est devenu obsolète

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import visu.columns_labels as columns_labels
CELLWIDTH=100
CELLHEIGHT=30



class Ui_MainWindow(QtWidgets.QWidget):

    #custom signal
    read_value = pyqtSignal(int,int,str)
    return_value = pyqtSignal(int,int,str)
    print_input = pyqtSignal(int,int)

    def setupUi(self, MainWindow,matrix):
        #Initialisation
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editLineLayout = QtWidgets.QHBoxLayout()
        self.editLineLayout.setObjectName('editLineLayout')

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setStyleSheet("item:{border-top-width: 200 px}")

        self.functionButton = QtWidgets.QToolButton(self.centralwidget)
        self.functionButton.setObjectName("functionButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.editLineLayout.addWidget(self.functionButton)
        self.editLineLayout.addWidget(self.lineEdit)

        self.verticalLayout.addLayout(self.editLineLayout)

        #On ajuste le nombre de colonnes/lignes en fonction de la taille de l'écran
        self.screen = QtWidgets.QDesktopWidget()
        self.initialRowsNumber=int(2*self.screen.height()/CELLHEIGHT)
        self.initialColumnsNumber=int(2*self.screen.width()/CELLWIDTH)
        self.tableWidget.setColumnCount(self.initialColumnsNumber)
        self.tableWidget.setRowCount(self.initialRowsNumber)
        matrix.addRows(self.initialRowsNumber-1)
        matrix.addColumns(self.initialColumnsNumber-1)

        #On attribue un identifiant à chaques colonnes
        for k in range(self.initialRowsNumber):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(k,item)

        #On attribue un identifiant à chaques lignes
        for k in range(self.initialColumnsNumber):
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

        self.setup(MainWindow, matrix)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup(self, MainWindow, matrix):
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

        #On ajoute des lignes à la fin si la barre VERTICALE de scrolling est en bas
        verticalscrollbar=self.tableWidget.verticalScrollBar()
        def ajoutRows():
            if verticalscrollbar.value()==verticalscrollbar.maximum():
                for _ in range(self.initialRowsNumber//3):
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                    matrix.addRow()
        verticalscrollbar.valueChanged.connect(ajoutRows)

        #On ajoute des colonnes à la fin si la barre HORIZONTALE de scrolling est en bas (il faut cette fois renommer les colonnes)
        horizontalscrollbar=self.tableWidget.horizontalScrollBar()
        def ajoutColumns():
            if horizontalscrollbar.value()==horizontalscrollbar.maximum():
                for _ in range(self.initialColumnsNumber//3):
                    self.tableWidget.insertColumn(self.tableWidget.columnCount())
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(self.tableWidget.columnCount()-1, item)
                    item = self.tableWidget.horizontalHeaderItem(self.tableWidget.columnCount()-1)
                    columns_labels.add(columnsLabels,1)
                    item.setText(_translate("MainWindow", columnsLabels[self.tableWidget.columnCount()-1]))
                    matrix.addColumn()
        horizontalscrollbar.valueChanged.connect(ajoutColumns)

        self.functionButton.setText(_translate("MainWindow", "..."))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuFichier.setTitle(_translate("MainWindow", "Menu1"))
        self.menuSsmenu1.setTitle(_translate("MainWindow", "ssmenu1"))
        self.menuSsmenu2.setTitle(_translate("MainWindow", "ssmenu2"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionOuvrir.setToolTip(_translate("MainWindow", "infobulle"))
        self.actionAction1.setText(_translate("MainWindow", "action1"))
        self.actionAction2.setText(_translate("MainWindow", "action2"))
        self.actionAction2_1.setText(_translate("MainWindow", "action21"))
        self.tableWidget.setDragDropMode(self.tableWidget.DragDrop) #Autorise le drag and drop ??

        #Envoi la coordonnée de la cellule changée et le nouvel item
        def cell_changed():
            self.read_value.emit(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),
                                 self.tableWidget.currentItem().text())
        self.tableWidget.cellChanged.connect(cell_changed)

        def change_cell(x, y, value):
            self.tableWidget.item(x,y).setText(value)
        self.return_value.connect(change_cell)

        # Affiche le input dans la ligne d'edition
        def cell_clicked():
            self.print_input.emit(self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        self.tableWidget.cellClicked.connect(cell_clicked)
        self.tableWidget.cellChanged.connect(cell_clicked)

        def changeLineEdit(x,y):
            input= matrix.getCell(x,y).input if len(matrix.getCell(x,y).input)>0 else matrix.getCell(x,y).value
            self.lineEdit.setText(input)
        self.print_input.connect(changeLineEdit)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized() #Pour agrandir au max la fenetre
    sys.exit(app.exec_())



