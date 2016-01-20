from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

def barDiagramme(data):
    plt.clf()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    abscisse = data[0]
    ordonnee = data[1:]
    for i in range(len(ordonnee)):
        for j in range(len(ordonnee[i])):
            ordonnee[i][j] = float(ordonnee[i][j])
    barWidth = .5/len(ordonnee)
    x0 = range(len(abscisse))
    for k in range(len(ordonnee)):
        couleur = colors[k%len(colors)]
        x = [i + barWidth*k for i in x0]
        plt.bar(x, ordonnee[k], width = barWidth, color = couleur, linewidth = 1)
    plt.xticks([i + .5/2 for i in range(len(abscisse))], abscisse, rotation = 45)
    plt.show()

#Partie concernant la sélection des donnees
def graph_selector(current_row,ui_mainwindow,statusBar,network,ui_graphwindow):
    ui_mainwindow.lineEdit.blockSignals(True) #Pour éviter les interactions de la lineEdit pendant la selection
    if current_row==0:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>abscisses</b></html>")
        btn_validate1 = QtWidgets.QPushButton("Valider")
        btn_validate1.clicked.connect(lambda : abscisseSelection(btn_validate1, ui_mainwindow, statusBar, network,ui_graphwindow, current_row))
        statusBar().addWidget(btn_validate1)
        print('vous avez choisi les courbes')
    elif current_row==1:
        print('vous avez choisi l histogramme')
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>labels</b></html>")
        btn_validate1 = QtWidgets.QPushButton("Valider")
        btn_validate1.clicked.connect(lambda : abscisseSelection(btn_validate1, ui_mainwindow, statusBar, network, ui_graphwindow, current_row))
        statusBar().addWidget(btn_validate1)
    elif current_row==2:
        print('vous avez choisi ')
        pass
    else:
        pass

def abscisseSelection(btn_validate1, ui_mainwindow, statusBar, network,graphwindow, current_row):
    data = []
    abscisse = []
    for item in ui_mainwindow.tableWidget.selectedItems():
        abscisse.append(network.getCell(item.row(), item.column()))
    data.append(abscisse)
    b = True
    for i in range(1, len(abscisse)):
        if abscisse[0].x == abscisse[i].x or abscisse[0].y == abscisse[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            b = False
            break
    if b:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>ordonnées</b></html>")
        statusBar().removeWidget(btn_validate1)
        btn_validate = QtWidgets.QPushButton("Valider")
        btn_validate.clicked.connect(lambda : ordonneesSelection([btn_validate], data, ui_mainwindow, statusBar, network, graphwindow, current_row))
        statusBar().addWidget(btn_validate)
    statusBar().removeWidget(btn_validate1)

def ordonneesSelection(btnList, data, ui_mainwindow, statusBar, network, graphwindow, current_row):
    for btn in btnList:
        statusBar().removeWidget(btn)
    ordonnee = []
    for item in ui_mainwindow.tableWidget.selectedItems():
        ordonnee.append(network.getCell(item.row(), item.column()))
    data.append(ordonnee)
    b = True
    for i in range(1, len(ordonnee)):
        if ordonnee[0].x == ordonnee[i].x or ordonnee[0].y == ordonnee[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            b = False
            break
    if b:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>ordonnées</b></html>")
    btn_tracer=QtWidgets.QPushButton("Tracer")
    statusBar().addWidget(btn_tracer)
    btn_ajouter=QtWidgets.QPushButton("Ajouter")
    statusBar().addWidget(btn_ajouter)
    btnList=[btn_ajouter,btn_tracer]
    ui_mainwindow.indicator.setText("<html>Pour tracer le graphique appuyez sur <b>Tracer</b> sinon pour superposer les graphiques, <i><font color='red'>effectuez une nouvelle sélection</font></i> puis appuyez sur <b>Ajouter</b></html>")
    btn_ajouter.clicked.connect(lambda : ordonneesSelection(btnList, data, ui_mainwindow, statusBar, network, graphwindow, current_row))
    btn_tracer.clicked.connect(lambda : mainGraphFunction(data, graphwindow,btnList,statusBar, ui_mainwindow, network, current_row))



#Tracé des courbes.
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
def mainGraphFunction(L,ui_graphwindow,btn_List,statusBar, ui_mainwindow, network, A):
    ui_mainwindow.indicator.setText("")
    ui_mainwindow.lineEdit.setText(network.getCell(ui_mainwindow.tableWidget.currentRow(),ui_mainwindow.tableWidget.currentColumn()).input)
    ui_mainwindow.lineEdit.blockSignals(False)
    for btn in btn_List:
            statusBar().removeWidget(btn)
    New_list=[]
    for list in L:
        New_list.append([x.value for x in list])
    if A == 0:
        courbe(New_list, ui_graphwindow, A)
    if A == 1:
        barDiagramme(New_list)

def courbe(L, ui_graphwindow, A):
    if len(L)==2:
        color=color_chooser(ui_graphwindow.combobox)
        plt.plot(L[0],L[1],color)
        print(L)
    else:

        for i in range(1,len(L)):
            plt.plot(L[0],L[i])
        plt.show()

def close_graph():
    plt.close()

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






