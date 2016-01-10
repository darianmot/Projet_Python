from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

def mainGraphFunction(L1, L2, A):
    if A == 0:
        x = []
        y = []
        for cell in L1:
            x.append(cell.value)
        for cell in L2:
            y.append(cell.value)
        plt.plot(x, y)
        plt.show()



class Ui_MainWindowgraph(object):


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
        self.circulaire=QtWidgets.QLabel(self.centralwidget)
        self.circulaire.setObjectName('label_circulaire')
        self.circulaire.setText('DIAGRAMME CIRCULAIRE')


        #ajout de widget aux layouts
        self.horizontalLayout_5.addWidget(self.listView)
        self.lastlayout.addWidget(self.circulaire)
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

        #valeur des ordonnées ymin ymax et layout associée

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
        #les connexions
        self.listView.itemClicked.connect(image)
        self.buttonBox.rejected.connect(quit)
        self.buttonBox.accepted.connect(quit)

    #
    # #selecteur de graphique
    # def chosentype(self):
    #     A=self.listView.currentRow()
    #     xtitle=self.lineEdit_2.text()
    #     ytitle=self.lineEdit_3.text()
    #     titleplot=self.lineEdit.text()
    #     color=self.combobox.currentText()
    #     explode=self.explode.text()
    #
    #     def colorchooser(color):
    #         if color=='rouge':
    #             color='r'
    #         elif color=='bleu':
    #             color='b'
    #         elif color=='jaune':
    #             color='y'
    #         elif color=='violet':
    #             color='p'
    #         elif color=='orange':
    #             color='o'
    #         elif color=='vert':
    #             color='g'
    #         else:
    #             color='b'
    #         return color


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graphiques"))
        self.label_4.setText(_translate("MainWindow", "     TITLE       "))
        self.label_2.setText(_translate("MainWindow", "    X AXIS TITLE"))

        self.label.setText(_translate("MainWindow", "    Y AXIS TITLE"))





