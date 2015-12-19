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

        #Description
        self.decriptionLayout = QtWidgets.QHBoxLayout()
        self.decriptionLayout.setObjectName("decriptionLayout")
        self.Description = QtWidgets.QLabel(Dialog)
        self.Description.setObjectName("Description")
        self.decriptionLayout.addWidget(self.Description)
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
            if isFunValid(name,description,evaluation):
                self.sendFunData.emit(name,description,evaluation,category)
                Dialog.accept()
                Dialog.close()

        self.buttonBox.accepted.connect(quit)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ajouter une fonction"))
        self.Nom.setText(_translate("Dialog", "Nom : "))
        self.Description.setText(_translate("Dialog", "Description : "))
        self.f_eval.setText(_translate("Dialog", "f(args) =  "))
        self.category.setText(_translate("Dialog", "Category : "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

