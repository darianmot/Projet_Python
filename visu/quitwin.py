# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quitwin.ui'
#
# Created: Tue Jan 19 16:42:19 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_quitwin(object):
    def setupUi(self, quitwin):
        quitwin.setObjectName("quitwin")
        quitwin.resize(365, 100)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/appIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        quitwin.setWindowIcon(icon)
        quitwin.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.widget = QtWidgets.QWidget(quitwin)
        self.widget.setGeometry(QtCore.QRect(20, 10, 336, 77))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(quitwin)
        self.buttonBox.accepted.connect(quitwin.accept)
        self.buttonBox.rejected.connect(quitwin.reject)
        QtCore.QMetaObject.connectSlotsByName(quitwin)

    def retranslateUi(self, quitwin):
        _translate = QtCore.QCoreApplication.translate
        quitwin.setWindowTitle(_translate("quitwin", "Enacell - Avertissement"))
        self.label.setText(_translate("quitwin", "Votre travail n\'est pas enregistré."))
        self.label_2.setText(_translate("quitwin", "Que voulez vous faire ?"))

