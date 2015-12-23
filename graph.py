from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
def graph(listeValue,ordonnée,abscisse,title,xmin,xmax,ymin,ymax,color):
    newliste=[x.value for x in listeValue]
    plt.plot[newliste,color]
    plt.ylabel(ordonnée)
    plt.xlabel(abscisse)
    plt.title(title)
    plt.axis(xmin,xmax,ymin,ymax)
    plt.show()


# a=input('image')
# print('a')
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("graphs")
#         MainWindow.resize(605, 400)
#         MainWindow.setMaximumSize(QtCore.QSize(10000, 10000))
#         #layout
#         self.mylayout=QtWidgets.QVBoxLayout()
#         self.mylayout.setObjectName('mylayout')
#         self.mysecondlayout=QtWidgets.QVBoxLayout()
#         self.mysecondlayout.setObjectName('mysecondlayout')
#         #La liste des graphiques
#         self.listgraph = QtWidgets.QListWidget(MainWindow)
#         self.listgraph.setMinimumSize(QtCore.QSize(300, 10000))
#         self.listgraph.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
#         self.listgraph.setObjectName("Graphiques")
#         self.mysecondlayout.addWidget(self.listgraph)
#         #la description
#         self.descriptionimage=QtWidgets.QLabel(MainWindow)
#         self.descriptionimage.setMinimumSize(QtCore.QSize(1000,300))
#         pixmap=QtGui.QPixmap(a)
#         self.descriptionimage.setPixmap(pixmap)
#         self.mylayout.addWidget(self.descriptionimage)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("graphs", "graphs"))
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
#

