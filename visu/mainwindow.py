# ATTENTION : vu qu'on a modifié ce fichier, mainwindow.ui est devenu obsolète

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import pyqtSignal
import visu.columns_labels as columns_labels,random
CELLWIDTH=100
CELLHEIGHT=30
class MyRect(Qt.QRect):
    def mousePressEvent(self,event):
        event.accept()
        print('tot')




class MyTableWidget(QtWidgets.QTableWidget):

    read_value = pyqtSignal(int,int,str)
    return_value = pyqtSignal(int,int,str)
    print_input= pyqtSignal(int,int)

    def __init__(self,win,network):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setMouseTracking(True)
        #On ajuste le nombre de colonnes/lignes en fonction de la taille de l'écran
        self.screen = QtWidgets.QDesktopWidget()
        self.initialRowsNumber=int(2*self.screen.height()/CELLHEIGHT)
        self.initialColumnsNumber=int(2*self.screen.width()/CELLWIDTH)
        self.setColumnCount(self.initialColumnsNumber)
        self.setRowCount(self.initialRowsNumber)
        self.columnsLabels=columns_labels.generate(self.columnCount()) #generation de la liste des labels (colonnes)
        #On attribue un identifiant à chaques colonnes
        for k in range(self.initialRowsNumber):
            item = QtWidgets.QTableWidgetItem()
            self.setVerticalHeaderItem(k,item)
            item.setText(_translate("MainWindow",str(k+1)))

        #On attribue un identifiant à chaques lignes
        for k in range(self.initialColumnsNumber):
            item = QtWidgets.QTableWidgetItem()
            self.setHorizontalHeaderItem(k, item)
            item.setText(_translate("MainWindow", self.columnsLabels[k]))

        #On ajoute les celulles crées graphiquement au network
        network.addRows(self.initialRowsNumber-1)
        network.addColumns(self.initialColumnsNumber-1)

        #On ajoute des lignes à la fin si la barre VERTICALE de scrolling est en bas
        verticalscrollbar=self.verticalScrollBar()
        def ajoutRows():
            if verticalscrollbar.value()==verticalscrollbar.maximum():
                for _ in range(self.initialRowsNumber//3):
                    self.insertRow(self.rowCount())
                    network.addRow()
        verticalscrollbar.valueChanged.connect(ajoutRows)

        #On ajoute des colonnes à la fin si la barre HORIZONTALE de scrolling est en bas (il faut cette fois renommer les colonnes)
        horizontalscrollbar=self.horizontalScrollBar()
        def ajoutColumns():
            if horizontalscrollbar.value()==horizontalscrollbar.maximum():
                for _ in range(self.initialColumnsNumber//3):
                    self.insertColumn(self.columnCount())
                    item = QtWidgets.QTableWidgetItem()
                    self.setHorizontalHeaderItem(self.columnCount()-1, item)
                    item = self.horizontalHeaderItem(self.columnCount()-1)
                    columns_labels.add(self.columnsLabels,1)
                    item.setText(_translate("MainWindow", self.columnsLabels[self.columnCount()-1]))
                    network.addColumn()
        horizontalscrollbar.valueChanged.connect(ajoutColumns)

    def paintEvent(self, event):
        QtWidgets.QTableWidget.paintEvent(self,event)
        y = self.rowViewportPosition(self.currentRow())
        x=self.columnViewportPosition(self.currentColumn())
        length = self.columnWidth(self.currentColumn())
        height = self.rowHeight(self.currentRow())
        painter=QtGui.QPainter(self.viewport())
        pen = QtGui.QPen(QtGui.QColor(0,0,0))
        pen.setWidth(2)
        painter.setPen(pen)
        rect=MyRect(x+1, y+1, length-3, height-3)
        #painter.drawRect(x+1, y+1, length-3, height-3)
        painter.drawRect(rect)
        painter.setBrush((QtGui.QColor(0,0,0)))
        painter.drawRect(x+length-8,y+height-8,5,5)
        event.accept()


    #Fonction qui s'active lorque l'utilisateur finit d'editer un item
    def closeEditor(self, editor, hint):
        print('Editor closed')
        QtWidgets.QTableWidget.closeEditor(self,editor,hint)
        self.read_value.emit(self.currentRow(),self.currentColumn(),self.currentItem().text())
        self.print_input.emit(self.currentRow(),self.currentColumn())

    def keyPressEvent(self, event):
        QtWidgets.QTableWidget.keyPressEvent(self,event)
        self.print_input.emit(self.currentRow(),self.currentColumn())

#
# class Border():
#     def __init__(self, length, height):



class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self, MainWindow,network):
        #La fenetre
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        #La ligne d'édition
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")

        #Le tableau
        self.tableWidget = MyTableWidget(self.centralwidget,network)
        self.tableWidget.setObjectName("tableWidget")

        #Les bouttons
        self.functionButton = QtWidgets.QToolButton(self.centralwidget)
        self.functionButton.setObjectName("functionButton")

        #Les layouts
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editLineLayout = QtWidgets.QHBoxLayout()
        self.editLineLayout.setObjectName('editLineLayout')
        self.editLineLayout.addWidget(self.functionButton)
        self.editLineLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.editLineLayout)
        self.verticalLayout.addWidget(self.tableWidget)

        #La toolbox et le menu
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

        self.setup(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Signaux et slots
        #Envoi la coordonnée de la cellule changée et le nouvel item
        # def cell_changed():
        #     self.tableWidget.read_value.emit(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),
        #                          self.tableWidget.currentItem().text())
        # self.tableWidget.cell.connect(cell_changed)

        def change_cell(x, y, value):
            try:
                self.tableWidget.item(x,y).setText(value)
            except AttributeError as e:
                pass
        self.tableWidget.return_value.connect(change_cell)

        # Affiche le input dans la ligne d'edition
        def cell_clicked():
            self.tableWidget.print_input.emit(self.tableWidget.currentRow(),self.tableWidget.currentColumn())
        self.tableWidget.cellClicked.connect(cell_clicked)
        self.tableWidget.cellChanged.connect(cell_clicked)

        def changeLineEdit(x,y):
            self.lineEdit.setText(network.getCell(x,y).input)
        self.tableWidget.print_input.connect(changeLineEdit)

        def line_changed():
            self.tableWidget.read_value.emit(self.tableWidget.currentRow(),self.tableWidget.currentColumn(),
                                 self.lineEdit.text())
        self.lineEdit.editingFinished.connect(line_changed)
        self.lineEdit.returnPressed.connect(line_changed)

        # def selected_cells():
        #     print(self.tableWidget.selectedItems())
        # self.tableWidget.itemSelectionChanged.connect(selected_cells)

        # def cell_entered():
        #     print('toto')
        # self.tableWidget.cellEntered.connect(cell_entered)
        # view=QtWidgets.QGraphicsView()
        # scene=QtWidgets.QGraphicsScene()
        # item=QtWidgets.QGraphicsRectItem()
        #
        # view.setScene(self.scene)
    def setup(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EnaCell"))
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



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized() #Pour agrandir au max la fenetre
    sys.exit(app.exec_())



