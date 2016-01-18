from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm



#Partie concernant la sélection des donnees
def graph_selector(current_row,ui_mainwindow,statusBar,network,ui_graphwindow):
    if current_row==0:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>abscisses</b></html>")
        btn = QtWidgets.QPushButton("Valider")
        btn.clicked.connect(lambda : abscisseSelection(btn, ui_mainwindow, statusBar, network,ui_graphwindow))
        statusBar().addWidget(btn)
        print('vous avez choisi les courbes')
    elif current_row==1:
        print('vous avez choisi l histogramme')
        pass
    elif current_row==2:
        print('vous avez choisi ')
        pass
    else:
        pass

def abscisseSelection(btn, ui_mainwindow, statusBar, network,graphwindow):
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
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>abscisses</b></html>")
        statusBar().removeWidget(btn)
        btn2 = QtWidgets.QPushButton("Valider")
        btn2.clicked.connect(lambda : seconde_selection_de_donnees(btn2, L1, ui_mainwindow, statusBar, network,graphwindow))
        statusBar().addWidget(btn2)
    statusBar().removeWidget(btn)

def seconde_selection_de_donnees(btn2, L1, ui_mainwindow, statusBar, network,ui_graphwindow):
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
            L=[[x.value for x in L1],[y.value for y in L2]]
            add_graph(L,ui_mainwindow,statusBar,network,ui_graphwindow)
            ui_mainwindow.indicator.setText("La sélection est correcte")
        else:
            ui_mainwindow.indicator.setText("Erreur: Sélections de tailles différentes")
    statusBar().removeWidget(btn2)
    ui_mainwindow.lineEdit.setText(network.getCell(ui_mainwindow.tableWidget.currentRow(),ui_mainwindow.tableWidget.currentColumn()).input)
    ui_mainwindow.lineEdit.blockSignals(False)
    ui_mainwindow.indicator.setText("Voulez vous superposer une autre courbe? Si oui appuyez sur VALIDER sinon su ANNULER")

#fonction ajout d autres graphes
def add_graph(L,ui_mainwindow,statusBar,network,ui_graphwindow):
    list_to_plot=L
    btn_add=QtWidgets.QPushButton("Add")
    statusBar().addWidget(btn_add)
    btn_cancel=QtWidgets.QPushButton("Tracer")
    statusBar().addWidget(btn_cancel)

    #affichage du bouton valider pour selectionner une serie de valeurs en plus si l on a accepter d ajouter une autre serie de valeurs.
    def affichage_btn_add_cancel(statusBar):
        print('veuillez selectionner une nouvelle série de valeurs')
        ui_mainwindow.indicator.setText('->Veuillez selectionner une nouvelle série de valeurs s il vous plait')
        btn_validate=QtWidgets.QPushButton('validate')
        statusBar.addWidget(btn_validate)


        btn_validate.clicked.connect(plot_graph)
        btn_validate.clicked.connect(lambda : statusBar.removeWidget(btn_validate))

    #affichage du graphique
    def plot_graph():
        list_to_plot=add_liste(L)
        for i in range(0,int((len(list_to_plot)/2))):
            plt.plot(list_to_plot[2*i],list_to_plot[2*i+1])
            print(i)
        plt.show()
        print('graphique affiché')
        ui_mainwindow.indicator.setText('')
        add_graph(L,ui_graphwindow,statusBar,network,ui_graphwindow)

    #fonction d'ajout d une autre liste de valeurs aux autres deja selectionnees
    def add_liste(L):
        new_liste=[network.getCell(item.row(), item.column()).value for item in ui_mainwindow.tableWidget.selectedItems()]
        list_to_plot.append(L[0])
        list_to_plot.append(new_liste)
        return list_to_plot

    #supprime les boutons cancel et add dans le cas ou l on desire afficher une serie de valeur en plus
    def add_function():
         print('Vous voulez superposer une autre série de valeurs a celles deja existente')
         statusBar().removeWidget(btn_add)
         statusBar().removeWidget(btn_cancel)
         affichage_btn_add_cancel(statusBar())

    #fonction d annulation qui sort du processus d ajout
    def cancel():
         print('vous ne voulez pas ajouter dautres valeurs')
         statusBar().removeWidget(btn_add)
         statusBar().removeWidget(btn_cancel)
         ui_mainwindow.indicator.setText("")
         mainGraphFunction(list_to_plot,ui_graphwindow)
         ui_mainwindow.indicator.setText('')
    btn_add.clicked.connect(add_function)
    btn_cancel.clicked.connect(cancel)



#Tracé des courbes
def color_chooser(combobox):
    color=combobox.currentText()
    if color=='rouge':
        return 'red'
    elif color=='bleu':
        return 'blue'
    elif color=='orange':
        return 'orange'
    elif color=='jaune':
        return 'yellow'
    elif color=='noir':
        return 'black'
    elif color=='violet':
        return 'purple'
    else:
        return 'green'
def mainGraphFunction(L,ui_graphwindow):
    color=color_chooser(ui_graphwindow.combobox)
    plt.plot(L[0],L[1],color)
    plt.show()
def close_graph():
    plt.close()

#Fenetre de sélection
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
        self.courbe.setText('courbe')
        self.listView.addItem(self.courbe)

        self.histogramme=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.histogramme)
        self.histogramme.setText('histogramme')
        self.camembert=QtWidgets.QListWidgetItem()
        self.listView.addItem(self.camembert)
        self.camembert.setText('camembert')
        self.fonction_DD=QtWidgets.QListWidgetItem()
        self.fonction_DD.setText('F(X,Y)')
        self.listView.addItem(self.fonction_DD)
        self.listView.setCurrentRow(0)


        #ajout de widget aux layouts
        self.horizontalLayout_5.addWidget(self.listView)


        #images graphique et layout
        self.images = QtWidgets.QLabel()
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
        self.combobox.addItems(['rouge','bleu','jaune','orange','violet','noir','vert'])
        self.gridLayout.addWidget(self.combobox, 1, 1, 2, 1)
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
            courbe=QtGui.QPixmap('visu/icons/courbe.png')
            histogramme=QtGui.QPixmap('visu/icons/histogramme.jpg')
            camembert=QtGui.QPixmap('visu/icons/camembert.jpg')
            DD=QtGui.QPixmap('visu/icons/DD.png')
            A=self.listView.currentRow()
            if A==0:
                print('you chose courbe','image')
                self.images.setPixmap(courbe)
            elif A==1:
                print('you chose histogramme','image')
                self.images.setPixmap(histogramme)
            elif A==2:
                self.images.setPixmap(camembert)
                print('you chose a camembert','image')
            elif A==3:
                self.images.setPixmap(DD)
                print('you chose a 2D representation')
        def quit():
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






