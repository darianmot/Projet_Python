"""Fenetre de gestion des fonctions"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

class Ui_funwindow(QtWidgets.QWidget):
    def setupUi(self, funwindow,knownFunctions):
        funwindow.setObjectName("funwindow")
        funwindow.resize(546, 343)
        # a=pickle.dump(knownFunctions,open('save.p','wb'))
        # print(pickle.load(open('save.p','rb')))
        #Les layouts
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(funwindow)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("listLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        #La liste de fonctions
        self.listFun = QtWidgets.QListWidget(funwindow)
        self.listFun.setMaximumSize(QtCore.QSize(231, 500))
        self.listFun.setObjectName("listFun")
        self.listLayout.addWidget(self.listFun)

        #Les catégories
        self.combobox=QtWidgets.QComboBox(funwindow)
        self.combobox.setObjectName('combobox')
        self.listLayout.addWidget(self.combobox)
        self.horizontalLayout_2.addLayout(self.listLayout)

        #Le cadre de droite
        # self.frame = QtWidgets.QFrame(funwindow)
        # self.frame.setMinimumSize(QtCore.QSize(231, 249))
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        # self.gridLayout = QtWidgets.QGridLayout(self.frame)
        # self.gridLayout.setObjectName("gridLayout")
        self.frameLayout=QtWidgets.QVBoxLayout()
        self.frameLayout.setObjectName("frameLayout")

        #Le nom de la fonction
        self.funName = QtWidgets.QLabel()
        self.funName.setObjectName("funName")
        # self.gridLayout.addWidget(self.funName, 0, 0, 1, 2)
        self.frameLayout.addWidget(self.funName)

        #La description
        self.description = QtWidgets.QLabel()
        self.description.setObjectName("description")
        # self.gridLayout.addWidget(self.description, 1, 0, 1, 1)
        self.frameLayout.addWidget(self.description)

        #Le label f(args)
        self.f_eval = QtWidgets.QLabel()
        self.f_eval.setObjectName("f_eval")
        self.horizontalLayout.addWidget(self.f_eval)

        #L'exrpression de la fonction
        self.expr = QtWidgets.QLabel()
        self.expr.setObjectName("expr")
        self.horizontalLayout.addWidget(self.expr)

        #Organisation des layout dans le cadre droit
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.frameLayout.addLayout(self.horizontalLayout)
        self.frameLayout.addStretch()
        self.horizontalLayout_2.addLayout(self.frameLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        #Les boutons ajouter/supprimer fonction
        self.toolAdd = QtWidgets.QToolButton(funwindow)
        self.toolAdd.setObjectName("toolAdd")
        self.horizontalLayout_3.addWidget(self.toolAdd)
        self.toolDel = QtWidgets.QToolButton(funwindow)
        self.toolDel.setObjectName("toolDel")
        self.horizontalLayout_3.addWidget(self.toolDel)
        #Supprime la fonction selectionnée
        def funDelete():
            print('suppression')
            currentCategory=self.combobox.currentIndex()
            function=self.functions[self.listFun.currentRow()]
            knownFunctions.removeFun(function)
            self.retranslateUi(funwindow,knownFunctions)
            self.combobox.setCurrentIndex(currentCategory)
        self.toolDel.clicked.connect(funDelete)

        #Un space item pour séparer les boutons du bas
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)

        #Les boutons Cancel/Ok
        self.pushOk = QtWidgets.QPushButton(funwindow)
        self.pushOk.setObjectName("pushOk")
        self.horizontalLayout_3.addWidget(self.pushOk)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        def quit():
            funwindow.close()
            self.retranslateUi(funwindow,knownFunctions)
        self.pushOk.released.connect(quit)

        #Finalisation
        self.retranslateUi(funwindow,knownFunctions)
        QtCore.QMetaObject.connectSlotsByName(funwindow)

    def retranslateUi(self, funwindow,knownFunctions):
        _translate = QtCore.QCoreApplication.translate
        funwindow.setWindowTitle(_translate("funwindow", "Functions"))
        self.listFun.setFocus()

        #La liste des fonctions
        self.functions=knownFunctions.getFunList()
        for k in range(len(self.functions)):
            item = QtWidgets.QListWidgetItem()
            self.listFun.addItem(item)
            item.setText(_translate("funwindow", self.functions[k].name))

        #Les catégories
        self.combobox.clear()
        for category in knownFunctions.getCategoryList():
            self.combobox.addItem(category)
        
        self.listFun.setCurrentRow(0)
        self.combobox.setCurrentText('All')
        self.toolAdd.setText(_translate("funwindow", "+"))
        self.toolDel.setText(_translate("funwindow", "-"))
        self.pushOk.setText(_translate("funwindow", "OK"))

        #Affiche les details de la fonction selectionnée
        def funSelected():
            k=self.listFun.currentRow()
            try:
                font=QtGui.QFont()
                font.setBold(True)
                font.setPointSize(20)
                self.funName.setFont(font)
                self.funName.setText(_translate("funwindow", "<html><head/><body><p align=\"center\">{}</p></body></html>".format(self.functions[k].name)))
                self.description.setText(_translate("funwindow", "Description : {}".format(self.functions[k].description)))
                self.f_eval.setText(_translate("funwindow", "{}(args)=".format(self.functions[k].name)))
                self.expr.setText(_translate("funwindow", self.functions[k].output))
            except IndexError:
                self.funName.setText(_translate("funwindow", "Pas de fonction selectionnée"))
                self.description.clear()
                self.f_eval.clear()
                self.expr.clear()
        self.listFun.itemSelectionChanged.connect(funSelected)

        #Affiche les fonctions de la catégorie selectionnée
        def categorySelected():
            currentCategory=self.combobox.currentText()
            if currentCategory=='All':
                self.functions=knownFunctions.getFunList()
            else:
                self.functions=knownFunctions.functionOfCategory(currentCategory)
            self.listFun.clear()
            for k in range(len(self.functions)):
                item = QtWidgets.QListWidgetItem()
                self.listFun.addItem(item)
                item.setText(_translate("funwindow", self.functions[k].name))
            self.listFun.setCurrentRow(0)
            funSelected()
        self.combobox.currentIndexChanged.connect(categorySelected)
        categorySelected()

