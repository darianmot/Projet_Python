# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
class Ui_Dialog(QtWidgets.QWidget):
    sendFunData=pyqtSignal(str,str,str,str)

    def setupUi(self, Dialog,knownFunctions):
        Dialog.setObjectName("Dialog")
        Dialog.resize(537, 323)

        #Layouts
        self.buttonsLayout = QtWidgets.QHBoxLayout(Dialog)
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        #Nom de la fonction
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.nameLayout.setObjectName("nameLayout")
        self.Nom = QtWidgets.QLabel(Dialog)
        self.Nom.setObjectName("Nom")
        self.nameLayout.addWidget(self.Nom)
        self.nameEdit = QtWidgets.QLineEdit(Dialog)
        self.nameEdit.setObjectName("nameEdit")
        self.nameLayout.addWidget(self.nameEdit)
        self.verticalLayout.addLayout(self.nameLayout)

        #Label Error
        self.nameError = QtWidgets.QLabel()
        self.nameError.setObjectName("nameError")
        self.verticalLayout.addWidget(self.nameError)
        self.nameError.setMaximumHeight(40)
        self.nameError.hide()

        #Description
        self.decriptionLayout = QtWidgets.QHBoxLayout()
        self.decriptionLayout.setObjectName("decriptionLayout")
        self.description = QtWidgets.QLabel(Dialog)
        self.description.setObjectName("Description")
        self.decriptionLayout.addWidget(self.description)
        self.descriptionEdit = QtWidgets.QLineEdit(Dialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.decriptionLayout.addWidget(self.descriptionEdit)
        self.verticalLayout.addLayout(self.decriptionLayout)

        #Evaluation
        self.evaluationLayout = QtWidgets.QHBoxLayout()
        self.evaluationLayout.setObjectName("evaluationLayout")
        self.f_eval = QtWidgets.QLabel(Dialog)
        self.f_eval.setObjectName("f_eval")
        self.evaluationLayout.addWidget(self.f_eval)
        self.evalEdit = QtWidgets.QLineEdit(Dialog)
        self.evalEdit.setObjectName("evalEdit")
        self.evaluationLayout.addWidget(self.evalEdit)
        self.verticalLayout.addLayout(self.evaluationLayout)

        #Category
        self.categoryLayout = QtWidgets.QHBoxLayout()
        self.evaluationLayout.setObjectName("categoryLayout")
        self.category=QtWidgets.QLabel(Dialog)
        self.category.setObjectName("category")
        self.combobox=QtWidgets.QComboBox()
        self.combobox.setObjectName("combobox")
        l=knownFunctions.getCategoryList()
        l.remove('All')
        for category in l:
            self.combobox.addItem(category)
        self.categoryLayout.addWidget(self.category)
        self.categoryLayout.addWidget(self.combobox)
        self.verticalLayout.addLayout(self.categoryLayout)

        #Boutons Cancel/Ok
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonsLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        forbidListName=[]
        def isFunValid(name,description,evaluation):
            if not (bool(name) or bool(description) or bool(evaluation)) or name in forbidListName:#Si un des éléments est vide ou le nom n'est pas valide
                return False
            else:
                return True
        
        def quit():
            name=self.nameEdit.text()
            description=self.descriptionEdit.text()
            evaluation=self.evalEdit.text()
            category=self.combobox.currentText()
            if knownFunctions.isFunValid(name,evaluation):
                self.retranslateUi(Dialog)
                self.sendFunData.emit(name,description,evaluation,category)
                Dialog.accept()
                Dialog.close()
            else:
                if name=="":
                    self.nameError.setText("<font color='red'>Le nom ne peut être vide</font>")
                    self.nameError.show()
                print('Fonction non valide')

        self.buttonBox.accepted.connect(quit)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.nameEdit.setFocus()
        Dialog.setWindowTitle(_translate("Dialog", "Ajouter une fonction"))
        self.Nom.setText(_translate("Dialog", "Nom : "))
        self.nameEdit.clear()
        self.description.setText(_translate("Dialog", "Description : "))
        self.descriptionEdit.clear()
        self.f_eval.setText(_translate("Dialog", "f(args) =  "))
        self.evalEdit.clear()
        self.category.setText(_translate("Dialog", "Category : "))



