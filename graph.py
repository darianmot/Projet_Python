from PyQt5 import QtWidgets
import matplotlib.pyplot as plt


# Partie concernant la sélection des donnees

def graph_selector(current_row, ui_mainwindow, statusBar, network, ui_graphwindow):
    ui_mainwindow.lineEdit.blockSignals(True)  # Pour éviter les interactions de la lineEdit pendant la selection
    btn_validate1 = QtWidgets.QPushButton("Valider")
    btn_validate1.clicked.connect(lambda: abscisseSelection(btn_validate1, ui_mainwindow, statusBar, network, ui_graphwindow, current_row))
    statusBar().addWidget(btn_validate1)
    if current_row == 0:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>abscisses</b></html>")
    elif current_row == 2:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>labels</b></html>")
    elif current_row == 3:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>labels</b></html>")
    elif current_row == 1:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>abscisses</b></html>")

def abscisseSelection(btn_validate1, ui_mainwindow, statusBar, network, graphwindow, current_row):
    data = []
    abscisse = []
    for item in ui_mainwindow.tableWidget.selectedItems():
        abscisse.append(network.getCell(item.row(), item.column()))
        print(item.row(), item.column())
    data.append(abscisse)
    key = True
    for i in range(1, len(abscisse)):
        if abscisse[0].x == abscisse[i].x or abscisse[0].y == abscisse[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            key = False
            break

    if key:
        ui_mainwindow.indicator.setText("<html>Sélectionnez la liste des <b>ordonnées</b></html>")
        statusBar().removeWidget(btn_validate1)
        btn_validate = QtWidgets.QPushButton("Valider")
        btn_validate.clicked.connect(lambda: ordonneesSelection([btn_validate], data, ui_mainwindow, statusBar, network, graphwindow, current_row))
        statusBar().addWidget(btn_validate)
    statusBar().removeWidget(btn_validate1)


def ordonneesSelection(btnList, data, ui_mainwindow, statusBar, network, graphwindow, current_row):
    for btn in btnList:
        statusBar().removeWidget(btn)
    ordonnee = []
    for item in ui_mainwindow.tableWidget.selectedItems():
        ordonnee.append(network.getCell(item.row(), item.column()))
    data.append(ordonnee)
    key = True
    for i in range(1, len(ordonnee)):
        if ordonnee[0].x == ordonnee[i].x or ordonnee[0].y == ordonnee[i].y:
            pass
        else:
            ui_mainwindow.indicator.setText("Erreur: veuillez selectionner une seule ligne ou colonne")
            key = False
            break
    if key:
        if current_row == 3:
            values = []
            lab = []
            l = len(data[1])
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            for i in range(l):
                if data[1][i].value is not None:
                    values.append(float(data[1][i].value) )
            for i in range(len(data[0])):
                if data[0][i].value is not None:
                    lab.append(data[0][i].value)
            plt.pie(values, labels = lab, colors = colors)
            plt.axis('equal')
            plt.title(graphwindow.lineEdit_3.text())
            plt.show()
            ui_mainwindow.indicator.setText("")
        else:
            btn_tracer = QtWidgets.QPushButton("Tracer")
            statusBar().addWidget(btn_tracer)
            btn_ajouter = QtWidgets.QPushButton("Ajouter")
            statusBar().addWidget(btn_ajouter)
            btnList = [btn_ajouter, btn_tracer]
            ui_mainwindow.indicator.setText(
                "<html>Pour tracer le graphique appuyez sur <b>Tracer</b> sinon pour superposer les graphiques, <i><font color='red'>effectuez une nouvelle sélection</font></i> puis appuyez sur <b>Ajouter</b></html>")
            btn_ajouter.clicked.connect(
                lambda: ordonneesSelection(btnList, data, ui_mainwindow, statusBar, network, graphwindow, current_row))
            btn_tracer.clicked.connect(
                lambda: mainGraphFunction(data, graphwindow, btnList, statusBar, ui_mainwindow, network, current_row))


# Choix de la couleur
def color_chooser(combobox):
    color = combobox.currentText()
    if color == 'rouge':
        return 'r'
    elif color == 'bleu':
        return 'b'
    elif color == 'cyan':
        return 'c'
    elif color == 'jaune':
        return 'y'
    elif color == 'noir':
        return 'k'
    elif color == 'violet':
        return 'm'
    else:
        return 'g'


# Tracé du graphique selon les options selectionnées
def mainGraphFunction(L, ui_graphwindow, btn_List, statusBar, ui_mainwindow, network, selectedgraph):
    ui_mainwindow.indicator.setText("")
    ui_mainwindow.lineEdit.setText(network.getCell(ui_mainwindow.tableWidget.currentRow(), ui_mainwindow.tableWidget.currentColumn()).input)
    ui_mainwindow.lineEdit.blockSignals(False)
    for btn in btn_List:
        statusBar().removeWidget(btn)
    New_list = []
    for list in L:
        New_list.append([x.value for x in list if x.value is not None])
    if selectedgraph == 0:
        courbe(New_list, ui_graphwindow)
    if selectedgraph == 1:
        nuage(New_list, ui_graphwindow)
    if selectedgraph == 2:
        barDiagramme(New_list, ui_graphwindow)
    plt.ylabel(ui_graphwindow.lineEdit.text())
    plt.xlabel(ui_graphwindow.lineEdit_2.text())
    plt.title(ui_graphwindow.lineEdit_3.text())
    plt.show()

# Trace un nuage de points liés
def courbe(data, ui_graphwindow):
    if len(data) == 2:
        color = color_chooser(ui_graphwindow.combobox)
        plt.plot(data[0], data[1], color + 'o-')
    else:
        for i in range(1, len(data)):
            plt.plot(data[0], data[i], 'o-')
    plt.grid()

#Trace un nuage de point
def nuage(data, ui_graphwindow):
    if len(data) == 2:
        color = color_chooser(ui_graphwindow.combobox)
        plt.plot(data[0], data[1], color + 'o')
    else:
        for i in range(1, len(data)):
            plt.plot(data[0], data[i], 'o')
    plt.grid()

# Trace un diagramme en bâton
def barDiagramme(data, ui_graphwindow):
    plt.clf()
    color = color_chooser(ui_graphwindow.combobox)
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    colors = [color] + [c for c in colors if c != color[0]]
    abscisse = data[0]
    ordonnee = data[1:]
    for i in range(len(ordonnee)):
        for j in range(len(ordonnee[i])):
            ordonnee[i][j] = float(ordonnee[i][j])
    barWidth = .5 / len(ordonnee)
    x0 = range(len(abscisse))
    for k in range(len(ordonnee)):
        couleur = colors[k % len(colors)]
        x = [i + barWidth * k for i in x0]
        plt.bar(x, ordonnee[k], width=barWidth, color = couleur, linewidth = 1)
    plt.xticks([i + .5 / 2 for i in range(len(abscisse))], abscisse, rotation = 45)