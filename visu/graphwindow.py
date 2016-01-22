from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal


#Fenetre de sélection..
class Ui_MainWindowgraph(QtWidgets.QWidget):

    okSignal = pyqtSignal(int)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 671)

        #création de la grille
        self.gridLayout = QtWidgets.QGridLayout(MainWindow)
        self.gridLayout.setObjectName("gridLayout")

        # 1introduction de layout dans la grille, celle du diagramme circulaire aussi
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lastlayout= QtWidgets.QHBoxLayout()
        self.lastlayout.setObjectName("lastlayout")
        self.lastlayout1=QtWidgets.QHBoxLayout()

        self.lastlayout1.setObjectName("lastlayout1")

        #liste des types de graphiques
        self.listView = QtWidgets.QListWidget()
        self.listView.setObjectName("listView")
        self.courbe=QtWidgets.QListWidgetItem()
        self.courbe.setText('Nuage de point lié')
        self.listView.addItem(self.courbe)
        self.nuage=QtWidgets.QListWidgetItem()
        self.nuage.setText('Nuage de point')
        self.listView.addItem(self.nuage)
        self.histogramme=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.histogramme)
        self.histogramme.setText('Diagramme en bâton')
        self.camembert=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.camembert)
        self.camembert.setText('Diagramme circulaire')
        self.listView.setCurrentRow(0)


        #ajout de widget aux layouts
        self.horizontalLayout_5.addWidget(self.listView)


        #images graphique et layout
        self.images = QtWidgets.QLabel()
        self.images.setObjectName("graphicsView")
        nuage=QtGui.QPixmap('visu/icons/approximation3.png')
        self.images.setPixmap(nuage)
        self.horizontalLayout_5.addWidget(self.images)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.lastlayout1,5,1,1,1)
        self.gridLayout.addLayout(self.lastlayout,5,0,1,1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #les labels et ligne d'éditions pour le titre
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit()
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)

        #la combobox  pour la couleur
        self.combobox=QtWidgets.QComboBox()
        self.combobox.addItems(['rouge','bleu','jaune','cyan','violet','noir','vert'])
        self.gridLayout.addWidget(self.combobox, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        #labels et layouts pour l'axe des abscisses
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 2, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel()
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)


        #label axe des ordonnees
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel()
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)

        #bouton ok et cancel
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 1)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #selecteur d'image
        def image():
            A=self.listView.currentRow()
            print(A)
            nuage_lié=QtGui.QPixmap('visu/icons/approximation3.png')
            histogramme=QtGui.QPixmap('visu/icons/diagramme_baton.png')
            camembert=QtGui.QPixmap('visu/icons/diagramme_circulaire.png')
            nuage_non_lié=QtGui.QPixmap('visu/icons/nuage_non_lié.png')

            A=self.listView.currentRow()
            if A==0:
                self.images.setPixmap(nuage_lié)
            elif A == 1:
                self.images.setPixmap(nuage_non_lié)
            elif A==2:
                self.images.setPixmap(histogramme)
            elif A==3:
                self.images.setPixmap(camembert)
        def quit():
            print('closing')
            MainWindow.close()

        def okGraph():
            self.okSignal.emit(self.listView.currentRow())


        #les connexions
        self.listView.itemSelectionChanged.connect(image)
        self.buttonBox.rejected.connect(quit)
        self.buttonBox.accepted.connect(okGraph)
        self.buttonBox.accepted.connect(quit)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graphiques"))
        self.label_4.setText(_translate("MainWindow", "     TITLE       "))
        self.label_2.setText(_translate("MainWindow", "    X AXIS TITLE"))
        self.label.setText(_translate("MainWindow", "    Y AXIS TITLE"))