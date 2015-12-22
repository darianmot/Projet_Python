# ATTENTION : vu qu'on a modifié ce fichier, mainwindow.ui est devenu obsolète

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import pyqtSignal
import visu.columns_labels as columns_labels,random
CELLWIDTH=100
CELLHEIGHT=30



class MyRect(Qt.QRect):
    def __init__(self):
        super().__init__()
        self.isSelected = False
        self.isUnder = False


class MyDelegate(QtWidgets.QItemDelegate):
    editorcreated=pyqtSignal()
    def __init__(self,table):
        super().__init__()
        self.table=table

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        print('Editor created')
        self.editorcreated.emit()
        return QtWidgets.QItemDelegate.createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex)


class EventEater(QtCore.QObject):
    def __init__(self,target):
        super().__init__()
        self.target = target

    def eventFilter(self, object, event):
        if event.type() == 2 and self.target.coin.contains(event.pos().x(),event.pos().y()):
            print('coin selected')
            self.target.coin.isSelected = True
            return True
        elif event.type() == 3 and self.target.coin.isSelected == True:
            print('coin released')
            self.target.coin.isSelected = False
            return True
        elif event.type() == 5:
            if self.target.coin.contains(event.pos().x(),event.pos().y()):
                self.target.coin.isUnder = True
            else:
                self.target.coin.isUnder = False
        return False


class MyItem(QtWidgets.QTableWidgetItem):
    pass


class MyTableWidget(QtWidgets.QTableWidget):

    read_value = pyqtSignal(int,int,str)
    return_value = pyqtSignal(int,int,str)
    print_input= pyqtSignal(int,int)

    def __init__(self,win,network):
        super().__init__()
        self.coin = MyRect()
        self.delegate=MyDelegate(self)
        self.setItemPrototype(MyItem())
        self.setItemDelegate(self.delegate)
        self.editorcount=0 #Permet de savoir si l'editeur de celulles est ouvert
        self.delegate.editorcreated.connect(self.itemeditoropened)
        _translate = QtCore.QCoreApplication.translate

        # Activation de la détection de la souris et du filtre d'événements pour la table
        self.setMouseTracking(True)
        self.filter = EventEater(self)
        self.viewport().installEventFilter(self.filter)

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

        self.coin.setRect(x+length-8,y+height-8,5,5)

        painter.drawRect(x+1, y+1, length-3, height-3)

        painter.setBrush((QtGui.QColor(0,0,0)))
        painter.drawRect(self.coin)
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        QtWidgets.QTableWidget.mouseMoveEvent(self,QMouseEvent)
        if self.coin.isSelected or self.coin.isUnder:
            self.setCursor(QtCore.Qt.CrossCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

    #Fonction qui s'active lorque l'utilisateur finit d'editer une cellule
    def closeEditor(self, editor, hint):
        print('Editor closed')
        self.editorcount-=1
        QtWidgets.QTableWidget.closeEditor(self,editor,hint)
        self.read_value.emit(self.currentRow(),self.currentColumn(),self.currentItem().text())
        self.print_input.emit(self.currentRow(),self.currentColumn())

    #Synchronise le input lorsque l'utilsateur change de cellule avec le clavier
    def keyPressEvent(self, event):
        QtWidgets.QTableWidget.keyPressEvent(self,event)
        self.print_input.emit(self.currentRow(),self.currentColumn())

    #Ajoute un incrément au compteur d'editeur si un éditeur est ouvert (connecte au signal editocreated du delegate)
    def itemeditoropened(self):
        self.editorcount+=1

    def isTapping(self):
        return self.editorcount!=0

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
        funIcon = QtGui.QIcon()
        funIcon.addPixmap(QtGui.QPixmap("visu/icons/functions.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.functionButton.setIcon(funIcon)

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

        MainWindow.setMenuBar(self.menubar)

        #Open action
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setText("Ouvrir")
        self.menu_ouvrir = QtWidgets.QAction(MainWindow)
        self.menu_ouvrir.setText("Ouvrir")
        openIcon = QtGui.QIcon()
        openIcon.addPixmap(QtGui.QPixmap("visu/icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOuvrir.setIcon(openIcon)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.menu_ouvrir.setIcon(openIcon)

        #Save Action
        self.actionenregistrer = QtWidgets.QAction(MainWindow)
        self.actionenregistrer.setText("Enregistrer")
        self.menu_enregistrer = QtWidgets.QAction(MainWindow)
        self.menu_enregistrer.setText("Enregistrer")
        saveIcon = QtGui.QIcon()
        saveIcon.addPixmap(QtGui.QPixmap("visu/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionenregistrer.setIcon(saveIcon)
        self.menu_enregistrer.setIcon(saveIcon)

        #Quit Action
        self.menu_quit = QtWidgets.QAction(MainWindow)
        self.menu_quit.setText("Quitter")
        quitIcon = QtGui.QIcon()
        quitIcon.addPixmap(QtGui.QPixmap("visu/icons/quit.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_quit.setIcon(quitIcon)



        self.toolBar.addAction(self.actionOuvrir)
        self.toolBar.addAction(self.actionenregistrer)
        self.toolBar.addSeparator()

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menuFichier.addAction(self.menu_ouvrir)
        self.menuFichier.addAction(self.menu_enregistrer)
        self.menuFichier.addAction(self.menu_quit)



        self.setup(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Signaux et slots
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

    def setup(self, MainWindow):
        self.tableWidget.setFocus()
        self.tableWidget.setCurrentCell(0,0)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EnaCell"))
        self.functionButton.setText(_translate("MainWindow", "..."))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))




