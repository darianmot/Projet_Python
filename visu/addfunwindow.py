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

        #Evaluation error
        self.evalError = QtWidgets.QLabel()
        self.evalError.setObjectName("evalError")
        self.verticalLayout.addWidget(self.evalError)
        self.evalError.setMaximumHeight(40)

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
        
        def quitok():
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
                if evaluation=="":
                    self.evalError.setText("<font color='red' size=-1><i>L'expression ne peut être vide<i/></font>")
                    self.evalError.show()
                if name=="":
                    self.nameError.setText("<font color='red' size=-1><i>Le nom ne peut être vide<i/></font>")
                    self.nameError.show()
                elif not(name.isalpha()):
                    self.nameError.setText("<font color='red' size=-1><i>Le nom ne peut contenir que des lettres<i/></font>")
                    self.nameError.show()
                elif name=="args":
                    self.nameError.setText("<font color='red' size=-1><i>'args' ne peut definir le nom d'une fonction<i/></font>")
                    self.nameError.show()
                else:
                    self.nameError.setText("<font color='red' size=-1><i>La fonction existe déjà<i/></font>")
                    self.nameError.show()
                print('Fonction non valide')

        def quitCancel():
            self.retranslateUi(Dialog)
            Dialog.reject()
        self.buttonBox.accepted.connect(quitok)
        self.buttonBox.rejected.connect(quitCancel)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.nameEdit.setFocus()
        Dialog.setWindowTitle(_translate("Dialog", "Ajouter une fonction"))
        self.Nom.setText(_translate("Dialog", "Nom : "))
        self.nameEdit.clear()
        self.nameError.hide()
        self.description.setText(_translate("Dialog", "Description : "))
        self.descriptionEdit.clear()
        self.f_eval.setText(_translate("Dialog", "f(args) =  "))
        self.evalEdit.clear()
        self.evalError.hide()
        self.category.setText(_translate("Dialog", "Category : "))



