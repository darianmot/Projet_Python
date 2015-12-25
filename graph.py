
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
def graph(listeabscisse,listeordonnée,ordonnée,abscisse,title,xmin,xmax,ymin,ymax,color):
    a=[int(x) for x in listeabscisse]
    b=[int(x) for x in listeordonnée]
    print(a,b)
    plt.plot(a, b)
    # plt.ylabel(ordonnée)
    # plt.xlabel(abscisse)
    # plt.title(title)
    #plt.axis(xmin,xmax,ymin,ymax)
    plt.show()



def chooseitemplot():
    #A=QtWidgets.QListWidget.selectedItems(a)
    #print(A)

    print('it ok')

def imp():
    print('you chose an other type of graphic')

list=[]
list2=[]
def cell(cells_selected,network):
    j=0
    if j==0:
        j=j+1

        for i in range(cells_selected.topRow(),cells_selected.bottomRow()+1):
            list.append(network.getCell(i, cells_selected.leftColumn()).value)
            list2.append(network.getCell(i,cells_selected.rightColumn()).value)
            print(list,list2)
            print('done')

    else:

        list.clear()
        list2.clear()
        for i in range(cells_selected.topRow(),cells_selected.bottomRow()+1):
            list.append(network.getCell(i, cells_selected.leftColumn()).value)
            list2.append(network.getCell(i,cells_selected.rightColumn()).value)
            print(list,list2)
            print('done')
    return(list,list2)
class Ui_MainWindowgraph(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 671)

        #création de la grille
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # 1introduction de layout dans la grille
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        #liste des types de graphiques
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setObjectName("listView")
        self.courbe=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.courbe)
        self.courbe.setText('courbe')
        self.histogramme=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.histogramme)
        self.histogramme.setText('histogramme')
        self.camembert=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.camembert)
        self.camembert.setText('camembert')


        #autre layout
        self.horizontalLayout_5.addWidget(self.listView)



        #images graphique et layout
        self.images = QtWidgets.QLabel(self.centralwidget)
        self.images.setObjectName("graphicsView")
        b=QtGui.QPixmap('visu/icons/courbe.png')
        self.images.setPixmap(b)
        self.horizontalLayout_5.addWidget(self.images)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 2)
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
        self.combobox.addItems(['rouge','bleu','jaune','orange','violet','noir','gris','vert'])
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

        #les xmin xmax  dans la spin box avec les layout associées label associées
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout.addWidget(self.doubleSpinBox)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.horizontalLayout.addWidget(self.doubleSpinBox_2)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

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
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_3)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_4)
        self.gridLayout.addLayout(self.horizontalLayout_6, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        #bouton ok et cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #selecteur d'image
        def image():
            courbe=QtGui.QPixmap('visu/icons/courbe.png')
            histogramme=QtGui.QPixmap('visu/icons/histogramme.jpg')
            camembert=QtGui.QPixmap('visu/icons/camembert.jpg')
            A=self.listView.currentRow()
            image=self.images
            if A==0:
                print('you choosed courbe','image')
                image.setPixmap(courbe)
            elif A==1:
                print('you choose histogramme','image')
                image.setPixmap(histogramme)
            elif A==2:
                image.setPixmap(camembert)
                print('you choose a camembert','image')
            else:
                print('nothing selected','image')

        #selecteur de graphique
        def chosentype():#en construction
            A=self.listView.currentRow()
            ymin=self.doubleSpinBox_3.value()
            ymax=self.doubleSpinBox_4.value()
            xmax=self.doubleSpinBox_2.value()
            xmin=self.doubleSpinBox.value()
            xtitle=self.lineEdit_2.text()
            ytitle=self.lineEdit_3.text()
            titleplot=self.lineEdit.text()
            color='blue'
            if A==0:
                graph(list,list2,ytitle,xtitle,titleplot,xmin,xmax,ymin,ymax,color)
                print('you choosed courbe','chosen type')
            elif A==1:
                print('you choose histogramme','chosen type')
            else:
                print('you choose a camembert','chosen type')

        def quit():
            MainWindow.close()
        #les connexions
        self.listView.itemClicked.connect(image)
        self.buttonBox.accepted.connect(chosentype)
        self.buttonBox.accepted.connect(quit)
        self.buttonBox.rejected.connect(quit)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "     Title"))
        self.label_2.setText(_translate("MainWindow", "     X axis title"))
        self.label_5.setText(_translate("MainWindow", "xmin"))
        self.label_6.setText(_translate("MainWindow", "xmax"))
        self.label.setText(_translate("MainWindow", "    Y axis title"))
        self.label_7.setText(_translate("MainWindow", "ymin"))
        self.label_8.setText(_translate("MainWindow", "ymax"))






