import cells_traitements.decomposition as decomposition
import visu.columns_labels as columns_labels
import copy
from PyQt5 import QtWidgets, Qt


# Renvoie le input à traiter dans la celulle situé rows lignes plus bas que la celulle initale dans le cas où l'utilisateur tire verticalement sur le coin
def verticalPull(inputDecomposed, rows):
    elementList = copy.copy(inputDecomposed[0])  # Pour ne pas changer sur place la decomposition initiale
    elementType = inputDecomposed[1]  # Ne changera pas
    for i in range(len(elementList)):
        if elementType[i] == 'cell':
            dollardcount = elementList[i].count('$')
            if not ((dollardcount == 1 and elementList[i][
                0] != '$') or dollardcount == 2):  # Si il n'y a pas de $ devant la partie numerique
                letters = ''.join([char for char in elementList[i] if char.isalpha()])
                n = len(letters) if elementList[i][0] != '$' else len(
                    letters) + 1  # Indique ou commence les chiffres dans la chaine
                elementList[i] = elementList[i][:n] + str(int(elementList[i][n:]) + rows)
    return ''.join(elementList)


# Renvoie le input à traiter dans la celulle situé à columns colonnes de la celulle initale dans le cas où l'utilisateur tire horizonatalement sur le coin
def horizontalPull(inputDecomposed, columns, labels):
    elementList = copy.copy(inputDecomposed[0])  # Pour ne pas changer sur place la decomposition initiale
    elementType = inputDecomposed[1]
    for i in range(len(elementList)):
        if elementType[i] == 'cell':
            if elementList[i][0] != '$':
                letters = ''.join([char for char in elementList[i] if char.isalpha()])
                n = columns_labels.getColumn(letters)  # On recupere le label de la colonne pour l'itérer columns fois
                newletters = columns_labels.getLabel(labels, n + columns)
                elementList[i] = newletters + elementList[i][len(letters):]  # On change la partie des lettres
    return ''.join(elementList)


# Change la value et le input des celulles lorsque la tirette est utilisée
def formuleExpanse(cells_selected, network, ui_mainwindow):
    if cells_selected.leftColumn() == cells_selected.rightColumn():
        column = cells_selected.rightColumn()
        r0 = cells_selected.topRow()  # Ligne initiale
        input = network.getCell(r0, column).input
        if len(input) == 0:
            pass
        elif input[0] != '=':
            for i in range(r0 + 1, cells_selected.bottomRow() + 1):
                if ui_mainwindow.tableWidget.item(i, column) == None:
                    ui_mainwindow.tableWidget.setItem(i, column, QtWidgets.QTableWidgetItem())
                ui_mainwindow.tableWidget.read_input.emit(i, column, input)
        else:
            decomposition0 = decomposition.decompo(input)
            for i in range(r0 + 1, cells_selected.bottomRow() + 1):
                rows = i - r0
                newinput = verticalPull(decomposition0, rows)
                if ui_mainwindow.tableWidget.item(i, column) == None:
                    ui_mainwindow.tableWidget.setItem(i, column, QtWidgets.QTableWidgetItem())
                ui_mainwindow.tableWidget.read_input.emit(i, column, newinput)
    elif cells_selected.topRow() == cells_selected.bottomRow():
        row = cells_selected.bottomRow()
        c0 = cells_selected.leftColumn()  # Colonne intiale
        input = network.getCell(row, c0).input
        if len(input) == 0:
            pass
        elif input[0] != '=':
            for i in range(c0 + 1, cells_selected.rightColumn() + 1):
                if ui_mainwindow.tableWidget.item(row, i) == None:
                    ui_mainwindow.tableWidget.setItem(row, i, QtWidgets.QTableWidgetItem())
                ui_mainwindow.tableWidget.read_input.emit(row, i, input)
        else:
            decomposition0 = decomposition.decompo(input)
            for i in range(c0 + 1, cells_selected.rightColumn() + 1):
                columns = i - c0
                newinput = horizontalPull(decomposition0, columns, ui_mainwindow.tableWidget.columnsLabels)
                if ui_mainwindow.tableWidget.item(row, i) == None:
                    ui_mainwindow.tableWidget.setItem(row, i, QtWidgets.QTableWidgetItem())
                ui_mainwindow.tableWidget.read_input.emit(row, i, newinput)


# Efface les rectangles verts, fin de l'effet tirette
def endTirette(ui_mainwindow, cells_selected):
    width = ui_mainwindow.tableWidget.columnWidth(ui_mainwindow.tableWidget.currentColumn())
    height = ui_mainwindow.tableWidget.rowHeight(ui_mainwindow.tableWidget.currentRow())
    x = cells_selected.leftColumn() * width
    y = cells_selected.topRow() * height
    range_width = cells_selected.rightColumn() - cells_selected.leftColumn() + 1
    range_height = cells_selected.bottomRow() - cells_selected.topRow() + 1
    reset_rect = Qt.QRect()
    reset_rect.setRect(x, y, range_width * width, range_height * height)
    ui_mainwindow.tableWidget.viewport().repaint(reset_rect)
