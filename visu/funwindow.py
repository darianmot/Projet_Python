# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'funwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_funwindow(object):
    def setupUi(self, funwindow,knownFunctions):
        funwindow.setObjectName("funwindow")
        funwindow.resize(546, 343)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(funwindow)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("listLayout")

        #On generere la liste de fonctions
        self.listFun = QtWidgets.QListWidget(funwindow)
        self.listFun.setMaximumSize(QtCore.QSize(231, 500))
        self.listFun.setObjectName("listFun")
        for k in range(len(knownFunctions.getFunList())):
            item = QtWidgets.QListWidgetItem()
            self.listFun.addItem(item)

        #Les catégories
        self.combobox=QtWidgets.QComboBox(funwindow)
        self.combobox.setObjectName('combobox')
        for category in knownFunctions.getCategoryList():
            self.combobox.addItem(category)

        self.listLayout.addWidget(self.combobox)
        self.listLayout.addWidget(self.listFun)
        self.horizontalLayout_2.addLayout(self.listLayout)
        self.frame = QtWidgets.QFrame(funwindow)
        self.frame.setMinimumSize(QtCore.QSize(231, 249))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.funName = QtWidgets.QLabel(self.frame)
        self.funName.setObjectName("funName")

        self.gridLayout.addWidget(self.funName, 0, 0, 1, 2)
        self.description = QtWidgets.QLabel(self.frame)
        self.description.setObjectName("description")
        self.gridLayout.addWidget(self.description, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.f_eval = QtWidgets.QLabel(self.frame)
        self.f_eval.setObjectName("f_eval")
        self.horizontalLayout.addWidget(self.f_eval)
        self.lineEdit = QtWidgets.QPlainTextEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.toolAdd = QtWidgets.QToolButton(funwindow)
        self.toolAdd.setObjectName("toolAdd")
        self.horizontalLayout_3.addWidget(self.toolAdd)
        self.toolDel = QtWidgets.QToolButton(funwindow)
        self.toolDel.setObjectName("toolDel")
        self.horizontalLayout_3.addWidget(self.toolDel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushCancel = QtWidgets.QPushButton(funwindow)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout_3.addWidget(self.pushCancel)
        self.pushOk = QtWidgets.QPushButton(funwindow)
        self.pushOk.setObjectName("pushOk")
        self.horizontalLayout_3.addWidget(self.pushOk)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.retranslateUi(funwindow,knownFunctions)
        self.pushCancel.released.connect(funwindow.close)
        self.pushOk.released.connect(funwindow.close)
        QtCore.QMetaObject.connectSlotsByName(funwindow)

    def retranslateUi(self, funwindow,knownFunctions):
        _translate = QtCore.QCoreApplication.translate
        funwindow.setWindowTitle(_translate("funwindow", "Functions"))

        self.functions=knownFunctions.getFunList()
        for k in range(len(self.functions)):
            item = self.listFun.item(k)
            item.setText(_translate("funwindow", self.functions[k].name))

        
        self.listFun.setCurrentRow(0)
        self.combobox.setCurrentText('All')
        self.toolAdd.setText(_translate("funwindow", "+"))
        self.toolDel.setText(_translate("funwindow", "-"))
        self.pushCancel.setText(_translate("funwindow", "Cancel"))
        self.pushOk.setText(_translate("funwindow", "OK"))

        #Affiche les details de la fonction selectionnée
        def funSelected():
            k=self.listFun.currentRow()
            self.funName.setText(_translate("funwindow", "<html><head/><body><p align=\"center\">{}</p></body></html>".format(self.functions[k].name)))
            self.description.setText(_translate("funwindow", "Description : {}".format(self.functions[k].description)))
            self.f_eval.setText(_translate("funwindow", "{}(args)=".format(self.functions[k].name)))
            self.lineEdit.setPlainText(_translate("funwindow", self.functions[k].output))
        self.listFun.itemClicked.connect(funSelected)

        def categorySelected():
            currentCategory=self.combobox.currentText()
            if currentCategory=='All':
                self.functions=knownFunctions.getFunList()
            else:
                self.functions=knownFunctions.functionOfCategory(currentCategory)
            funSelected()
            self.listFun.clear()
            for k in range(len(self.functions)):
                item = QtWidgets.QListWidgetItem()
                self.listFun.addItem(item)
                item.setText(_translate("funwindow", self.functions[k].name))
        self.combobox.currentIndexChanged.connect(categorySelected)
        categorySelected()