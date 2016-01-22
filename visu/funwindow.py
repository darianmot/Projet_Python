"""Fenetre de gestion des fonctions"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pickle


class Ui_funwindow(QtWidgets.QWidget):
    def setupUi(self, funwindow, knownFunctions):
        funwindow.setObjectName("funwindow")
        funwindow.resize(546, 343)
        # Les layouts
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

        # La liste de fonctions
        self.listFun = QtWidgets.QListWidget(funwindow)
        self.listFun.setMaximumSize(QtCore.QSize(100, 500))
        self.listFun.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.listFun.setObjectName("listFun")
        self.listLayout.addWidget(self.listFun)

        # Les catégories
        self.combobox = QtWidgets.QComboBox(funwindow)
        self.combobox.setObjectName('combobox')
        self.listLayout.addWidget(self.combobox)
        self.horizontalLayout_2.addLayout(self.listLayout)

        # Le cadre de droite
        self.frameLayout = QtWidgets.QVBoxLayout()
        self.frameLayout.setObjectName("frameLayout")

        # Le nom de la fonction
        self.funName = QtWidgets.QLabel()
        self.funName.setObjectName("funName")
        self.frameLayout.addWidget(self.funName)

        # La description
        self.descriptiontext = QtWidgets.QLabel()
        self.descriptiontext.setWordWrap(True)
        self.descriptiontext.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.descriptiontext.setObjectName("descriptiontext")
        self.frameLayout.addWidget(self.descriptiontext)

        # L'exrpression de la fonction
        self.expr = QtWidgets.QLabel()
        self.expr.setObjectName("expr")
        self.expr.setWordWrap(True)
        self.frameLayout.addWidget(self.expr)

        # Organisation des layout dans le cadre droit
        self.frameLayout.addStretch()
        self.horizontalLayout_2.addLayout(self.frameLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Les boutons ajouter/supprimer fonction
        self.toolAdd = QtWidgets.QToolButton(funwindow)
        self.toolAdd.setObjectName("toolAdd")
        self.horizontalLayout_3.addWidget(self.toolAdd)
        addIcon = QtGui.QIcon()
        addIcon.addPixmap(QtGui.QPixmap("visu/icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolAdd.setIcon(addIcon)
        self.toolDel = QtWidgets.QToolButton(funwindow)
        self.toolDel.setObjectName("toolDel")
        self.horizontalLayout_3.addWidget(self.toolDel)
        delIcon = QtGui.QIcon()
        delIcon.addPixmap(QtGui.QPixmap("visu/icons/del.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolDel.setIcon(delIcon)

        # Supprime la fonction selectionnée
        def funDelete():
            currentCategory = self.combobox.currentIndex()
            function = self.functions[self.listFun.currentRow()]
            print('Suppression de la fonction {}'.format(function.name))
            knownFunctions.removeFun(function)
            self.retranslateUi(funwindow, knownFunctions)
            self.combobox.setCurrentIndex(currentCategory)
            pickle.dump(knownFunctions, open('knownFunctions.p', 'wb'))

        self.toolDel.clicked.connect(funDelete)

        # Un space item pour séparer les boutons du bas
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)

        # Les boutons Cancel/Ok
        self.pushOk = QtWidgets.QPushButton(funwindow)
        self.pushOk.setObjectName("pushOk")
        self.horizontalLayout_3.addWidget(self.pushOk)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        def quit():
            funwindow.close()
            self.retranslateUi(funwindow, knownFunctions)

        self.pushOk.released.connect(quit)

        # Finalisation
        self.retranslateUi(funwindow, knownFunctions)
        QtCore.QMetaObject.connectSlotsByName(funwindow)

    def retranslateUi(self, funwindow, knownFunctions):
        _translate = QtCore.QCoreApplication.translate
        funwindow.setWindowTitle(_translate("funwindow", "Functions"))
        self.listFun.setFocus()

        # La liste des fonctions
        self.functions = knownFunctions.getFunList()
        for k in range(len(self.functions)):
            item = QtWidgets.QListWidgetItem()
            self.listFun.addItem(item)
            item.setText(_translate("funwindow", self.functions[k].name))

        # Les catégories
        self.combobox.clear()
        for category in knownFunctions.getCategoryList():
            self.combobox.addItem(category)

        self.listFun.setCurrentRow(0)
        self.combobox.setCurrentText('All')
        self.toolAdd.setToolTip(_translate("funwindow", "Ajouter une fonction"))
        self.toolDel.setToolTip(_translate("funwindow", "Supprimer une fonction"))
        self.pushOk.setText(_translate("funwindow", "OK"))

        # Affiche les details de la fonction selectionnée
        def funSelected():
            k = self.listFun.currentRow()
            try:

                self.funName.setText(_translate("funwindow",
                                                "<html><head/><body><h2><p align=\"center\"><b>{}<b/></h2></p></body></html>".format(
                                                    self.functions[k].name)))
                self.descriptiontext.setText((_translate("funwindow",
                                                         "<html><head/><body><b>Description : </b><i>{}</i></body></html>".format(
                                                             self.functions[k].description))))
                self.expr.setText(_translate("funwindow", str(self.functions[k].output)))
                self.funName.show()
                self.descriptiontext.show()
                self.expr.show()
            except IndexError:
                self.funName.setText(_translate("funwindow",
                                                "<html><head/><body><h2><p align=\"center\"><b><i>No functions<i/><b/></h2></p></body></html>"))
                self.descriptiontext.clear()
                self.expr.hide()

        self.listFun.itemSelectionChanged.connect(funSelected)

        # Affiche les fonctions de la catégorie selectionnée
        def categorySelected():
            currentCategory = self.combobox.currentText()
            if currentCategory == 'All':
                self.functions = knownFunctions.getFunList()
            else:
                self.functions = knownFunctions.functionOfCategory(currentCategory)
            self.listFun.clear()
            for k in range(len(self.functions)):
                item = QtWidgets.QListWidgetItem()
                self.listFun.addItem(item)
                item.setText(_translate("funwindow", self.functions[k].name))
            self.listFun.setCurrentRow(0)
            funSelected()

        self.combobox.currentIndexChanged.connect(categorySelected)
        categorySelected()
