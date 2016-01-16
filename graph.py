from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm



#Partie concernant la sélection des données
def graphiques(ui_mainwindow, statusBar, network, A, settings):
    ui_mainwindow.indicator.setText("Sélectionnez une ligne ou colonne et appuyez sur Valider")
    btn = QtWidgets.QPushButton("Valider")
    btn.clicked.connect(lambda : action1(btn, ui_mainwindow, statusBar, network, A, settings))
    statusBar().addWidget(btn)

def action1(btn, ui_mainwindow, statusBar, network, A, settings):
    ui_mainwindow.lineEdit.blockSignals(True) #Pour éviter les interactions de la lineEdit pendant la selection
    L1=[]
    for item in ui_mainwindow.tableWidget.selectedItems():
        L1.append(network.getCell(item.row(), item.column()))
    b = True
    for i in range(1, len(L1)):
        if L1[0].x == L1[i].x or L1[0].y == L1[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            b = False
            break
    if b:
        print(L1)
        ui_mainwindow.indicator.setText("Sélectionnez une nouvelle ligne ou colonne et appuyez sur Valider")
        statusBar().removeWidget(btn)
        btn2 = QtWidgets.QPushButton("Valider")
        btn2.clicked.connect(lambda : action2(btn2, L1, ui_mainwindow, statusBar, network, A, settings))
        statusBar().addWidget(btn2)
    statusBar().removeWidget(btn)

def action2(btn2, L1, ui_mainwindow, statusBar, network, A, settings):
    L2=[]
    for item in ui_mainwindow.tableWidget.selectedItems():
        L2.append(network.getCell(item.row(), item.column()))
    b = True
    for i in range(1, len(L2)):
        if L2[0].x == L2[i].x or L2[0].y == L2[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou une seule colonne")
            b = False
            break
    if b:
        print(L1, L2)
        if len(L1) == len(L2):
            mainGraphFunction(L1, L2, A, settings)
            ui_mainwindow.indicator.setText("La sélection est correcte")
            #add(L1,L2)

        else:
            ui_mainwindow.indicator.setText("Erreur: Sélections de tailles différentes")
    statusBar().removeWidget(btn2)
    ui_mainwindow.lineEdit.setText(network.getCell(ui_mainwindow.tableWidget.currentRow(),ui_mainwindow.tableWidget.currentColumn()).input)
    ui_mainwindow.lineEdit.blockSignals(False)

# def add(L1,L2):
#
#     ui_mainwindow.indicator.setText("voulez vous superposer une autre courbe?")
#     btn_add=QtWidgets.QPushButton("+add")
#     MainWindow.statusBar().addWidget(btn_add)
#     btn_cancel=QtWidgets.QPushButton("annuler")
#     MainWindow.statusBar().addWidget(btn_cancel)
#     def add_2():
#         MainWindow.statusBar().removeWidget(btn_add)
#         MainWindow.statusBar().removeWidget(btn_cancel)
#         graphiques()
#         graphic.close_graph()
#
#     def cancel():
#         MainWindow.statusBar().removeWidget(btn_add)
#         MainWindow.statusBar().removeWidget(btn_cancel)
#         ui_mainwindow.indicator.setText("")
#     btn_add.clicked.connect(add_2)
#     btn_cancel.clicked.connect(cancel)



#Tracé des courbes
def mainGraphFunction(L1, L2, A, settings):
    if A == 0:
        x = []
        y = []
        for cell in L1:
            x.append(cell.value)
        for cell in L2:
            y.append(cell.value)
        plt.plot(x, y)
        plt.show()
def close_graph():
    plt.close()

#Fenetre de sélection
class Ui_MainWindowgraph(QtWidgets.QWidget):

    okSignal = pyqtSignal(int,list)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 671)

        #création de la grille
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # 1introduction de layout dans la grille, celle du diagramme circulaire aussi
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lastlayout= QtWidgets.QHBoxLayout()
        self.lastlayout.setObjectName("lastlayout")
        self.lastlayout1=QtWidgets.QHBoxLayout()
        self.lastlayout1.setObjectName("lastlayout1")

        #liste des types de graphiques
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setObjectName("listView")
        self.explode=QtWidgets.QLineEdit(self.centralwidget)
        self.explode.setObjectName('explode')
        self.courbe=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.courbe)
        self.courbe.setText('courbe')
        self.histogramme=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.histogramme)
        self.histogramme.setText('histogramme')
        self.camembert=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.camembert)
        self.camembert.setText('camembert')
        self.fonction_DD=QtWidgets.QListWidgetItem()
        self.fonction_DD.setText('F(X,Y)')
        self.listView.addItem(self.fonction_DD)


        #ajout de widget aux layouts
        self.horizontalLayout_5.addWidget(self.listView)
        self.lastlayout.addWidget(self.explode)


        #images graphique et layout
        self.images = QtWidgets.QLabel(self.centralwidget)
        self.images.setObjectName("graphicsView")
        b=QtGui.QPixmap('visu/icons/courbe.png')
        self.images.setPixmap(b)
        self.horizontalLayout_5.addWidget(self.images)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.lastlayout1,5,1,1,1)
        self.gridLayout.addLayout(self.lastlayout,5,0,1,1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #les labels et ligne d'éditions pour le titre
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)

        #la combobox  pour la couleur
        self.combobox=QtWidgets.QComboBox(self.centralwidget)
        self.combobox.addItems(['rouge','bleu','jaune','orange','violet','noir','vert'])
        self.gridLayout.addWidget(self.combobox, 1, 1, 2, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        #labels et layouts pour l'axe des abscisses
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 2, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)


        #label axe des ordonnees
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        #bouton ok et cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 1)
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #selecteur d'image
        def image():
            courbe=QtGui.QPixmap('visu/icons/courbe.png')
            histogramme=QtGui.QPixmap('visu/icons/histogramme.jpg')
            camembert=QtGui.QPixmap('visu/icons/camembert.jpg')
            DD=QtGui.QPixmap('visu/icons/DD.png')
            A=self.listView.currentRow()
            image=self.images
            if A==0:
                print('you chose courbe','image')
                image.setPixmap(courbe)
            elif A==1:
                print('you chose histogramme','image')
                image.setPixmap(histogramme)
            elif A==2:
                image.setPixmap(camembert)
                print('you chose a camembert','image')
            elif A==3:
                image.setPixmap(DD)
                print('you chose a 2D representation')
        def quit():
            MainWindow.close()

        def okGraph():
            self.okSignal.emit(self.listView.currentRow(), ['fsdv', 'cds0', 'vcdhbs', 'b'])
        #les connexions
        self.listView.itemClicked.connect(image)
        self.buttonBox.rejected.connect(quit)
        self.buttonBox.accepted.connect(okGraph)
        self.buttonBox.accepted.connect(quit)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graphiques"))
        self.label_4.setText(_translate("MainWindow", "     TITLE       "))
        self.label_2.setText(_translate("MainWindow", "    X AXIS TITLE"))
        self.label.setText(_translate("MainWindow", "    Y AXIS TITLE"))





