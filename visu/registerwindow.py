# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/insaf/PycharmProjects/Projet_Python1/visu/untitled.ui'
#
# Created: Sat Dec 12 21:12:19 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!
import recOrd,sys
from PyQt5 import QtCore, QtGui, QtWidgets


class UI_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 440)
        MainWindow.setMaximumSize(QtCore.QSize(10000, 10000))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(490, 186, 85, 61))
        # self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 170, 361, 400))
        self.label.setObjectName("label")



        self.arbo_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.tree = QtWidgets.QFileDialog()
        self.arbo_layout.addWidget(self.tree)







        # self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        # self.textEdit.setGeometry(QtCore.QRect(10, 200, 401, 51))
        # self.textEdit.setObjectName("textEdit")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.tree.fileSelected.connect(MainWindow.close)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Open..."))
        #self.pushButton.setText(_translate("MainWindow", "Validate"))
        #self.label.setText(_translate("MainWindow", "Writte down the adress of the file"))

