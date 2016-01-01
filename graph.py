import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
def draw_surface(xmin,xmax,ymin,ymax,zmin,zmax,expression):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y, z = axes3d.get_test_data(0.05)
    ax.plot_surface(x, y,expression , rstride=8, cstride=8, alpha=0.3)
    #cset = ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
    #cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    #cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
    # ax.set_xlabel('X')
    # ax.set_xlim(xmin, xmax)
    # ax.set_ylabel('Y')
    # ax.set_ylim(ymin, ymax)
    # ax.set_zlabel('Z')
    # ax.set_zlim(zmin, zmax)
    plt.show()

def circulaire(nom,content,titre,explode):
    plt.pie(content,explode,nom,autopct='%1.1f%%',startangle=90,shadow=True)
    plt.title(titre)
    plt.axis('equal')
    plt.show()

def histogramme(ordonnées,xmin,xmax,ymin,ymax,color,abscisse,ordonné):
    plt.hist(ordonnées)
    plt.xlabel(abscisse)
    plt.ylabel(ordonné)
    plt.axis([xmin,xmax,ymin,ymax])
    plt.grid(True)
    plt.show()

def graph(listeabscisse,listeordonnée,ordonnée,abscisse,title,xmin,xmax,ymin,ymax,color):
    a=[float(x) for x in listeabscisse]
    b=[float(x) for x in listeordonnée]
    print(a,b)
    plt.plot(a, b,color)
    plt.ylabel(ordonnée)
    plt.xlabel(abscisse)
    plt.title(title)
    plt.axis([xmin,xmax,ymin,ymax])
    plt.show()

def cell(cells_selected,network):
        ligne1=cells_selected.topRow()
        ligne2=cells_selected.bottomRow()+1
        Ui_MainWindowgraph.données.abscisses=[0 for i in range(ligne1,ligne2)]
        Ui_MainWindowgraph.données.ordonnées=[0  for i in range(ligne1,ligne2)]
        print(Ui_MainWindowgraph.données.abscisses)
        for i in range(ligne1,ligne2):
            abs = network.getCell(i, cells_selected.leftColumn()).value
            ord = network.getCell(i,cells_selected.leftColumn()+1).value
            print(ord)
            Ui_MainWindowgraph.données.abscisses[i-ligne1]=abs
            Ui_MainWindowgraph.données.ordonnées[i-ligne1]=ord
            print(Ui_MainWindowgraph.données.abscisses,Ui_MainWindowgraph.données.ordonnées,'abscisse,ordonéée ')

class  datas(object):
    def __init__(self):
        self.ordonnées=[]
        self.abscisses= []

class Ui_MainWindowgraph(object):
    données=datas()

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
        self.doubleSpinBoxZmin=QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxZmin.setObjectName("zmin")
        self.doubleSpinBoxZmax=QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxZmax.setObjectName("zmax")
        self.zmin=QtWidgets.QLabel(self.centralwidget)
        self.zmin.setObjectName("Zmin")
        self.zmin.setText("Zmin")
        self.zmax=QtWidgets.QLabel(self.centralwidget)
        self.zmax.setObjectName("Zmin")
        self.zmax.setText("Zmax")

        #ajout de widget aux layouts
        self.horizontalLayout_5.addWidget(self.listView)
        self.lastlayout.addWidget(self.circulaire)
        self.lastlayout.addWidget(self.explode)
        self.lastlayout1.addWidget(self.zmin)
        self.lastlayout1.addWidget(self.doubleSpinBoxZmin)
        self.lastlayout1.addWidget(self.zmax)
        self.lastlayout1.addWidget(self.doubleSpinBoxZmax)

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
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 1)
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

        def quit():
            MainWindow.close()
        #les connexions
        self.listView.itemClicked.connect(image)
        self.buttonBox.rejected.connect(quit)
        self.buttonBox.accepted.connect(self.chosentype)
        self.buttonBox.accepted.connect(quit)

    #selecteur de graphique
    def chosentype(self):
        A=self.listView.currentRow()
        ymin=self.doubleSpinBox_3.value()
        ymax=self.doubleSpinBox_4.value()
        xmax=self.doubleSpinBox_2.value()
        xmin=self.doubleSpinBox.value()
        xtitle=self.lineEdit_2.text()
        ytitle=self.lineEdit_3.text()
        titleplot=self.lineEdit.text()
        color=self.combobox.currentText()
        explode=self.explode.text()
        def colorchooser(color):

            if color=='rouge':
                 color='r'
                 return color
            elif color=='bleu':
                color='b'
                return color
            elif color=='jaune':
                color='y'
                return color
            elif color=='violet':
                color='p'
                return color
            elif color=='orange':
                color='o'
                return color
            elif color=='vert':
                color='g'
                return color
            else:
                color='b'
                return color

        if A==0:
            print(colorchooser(color))
            print(Ui_MainWindowgraph.données.abscisses,'absci')
            graph(Ui_MainWindowgraph.données.abscisses,Ui_MainWindowgraph.données.ordonnées
                 ,ytitle,xtitle,titleplot,xmin,xmax,ymin,ymax,colorchooser(color))
            print('you choosed courbe','chosen type')
        elif A==1:
            print('you choose histogramme','chosen type')
            listlisible=[float(x) for x in Ui_MainWindowgraph.données.abscisses]
            histogramme(listlisible,xmin,xmax,ymin,ymax,colorchooser(color),xtitle,ytitle)
        elif A==2:
            textes=explode.split(',')
            textes=[float(x) for x in textes]
            textes=tuple(textes)
            circulaire(Ui_MainWindowgraph.données.abscisses,Ui_MainWindowgraph.données.ordonnées,xtitle,explode=textes)
            #en cours d amelioration pour ajout de nouvelles fonctionnalites
            print('you choose a camembert  chosen type')
        else:#a revoir
            expressions=[x for x in Ui_MainWindowgraph.données.abscisses]
            A=expressions[0].strip('')
            print(A)
            #draw_surface(5,5,5,5,5,5,A)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graphiques"))
        self.label_4.setText(_translate("MainWindow", "     TITLE       "))
        self.label_2.setText(_translate("MainWindow", "    X AXIS TITLE"))
        self.label_5.setText(_translate("MainWindow", "Xmin"))
        self.label_6.setText(_translate("MainWindow", "Xmax"))
        self.label.setText(_translate("MainWindow", "    Y AXIS TITLE"))
        self.label_7.setText(_translate("MainWindow", "Ymin"))
        self.label_8.setText(_translate("MainWindow", "Ymax"))






