try:
    import xlrd
    HASXLRD = True
except ImportError:
    HASXLRD = False
try:
    from xlwt import Workbook
    HASXLWT = True
except ImportError:
    HASXLWT = False
import csv, pickle, os
from PyQt5 import QtWidgets


# Renvoie un message d'erreur à l'indicator si les modules pour le .xls ne sont pas installés
def etatXls(window):
    if (not HASXLRD) and (not HASXLWT):
        window.indicator.setText("<html><head/><body>{0} - <font color='red'>Les modules 'xlrd' et 'xlwt' n'étant pas installés,\
        l'ouverture et l'exportation des fichiers en .xls sont impossibles.</font></body></html>".format(
            window.indicator.text()))
    elif not HASXLRD and HASXLWT:
        window.indicator.setText("<html><head/><body>{0} - <font color='red'>Le module 'xlrd' n'étant pas installé,\
        l'ouverture des fichiers en .xls est impossible.</font></body></html>".format(window.indicator.text()))
    elif HASXLRD and not HASXLWT:
        window.indicator.setText("<html><head/><body>{0} - <font color='red'>Le module 'xlwt' n'étant pas installé,\
        l'exportation des fichiers en .xls est impossible.</font></body></html>".format(window.indicator.text()))


def writter_xls(network, name):
    content = name + '.xls'
    binder = Workbook()  # creation of the binder
    sheet = binder.add_sheet('page')  # creation of the sheet
    for x in range(0, len(network.matrix[0])):  # writting of each cell
        for y in range(0, len(network.matrix)):
            sheet.write(y, x, network.getCell(y, x).value)
    binder.save(content)  # save file
    print('file saved')
    network.title = content


def reader_xls(file, ui_mainwindow, network):
    binder = xlrd.open_workbook(file)  # opening of the file as a binder
    sheets = binder.sheet_names()  # listing of sheet names
    sheet = binder.sheet_by_name(sheets[0])  # recovering of the i eme sheet
    network.reset(1, 1)
    network.addRows(sheet.nrows - 1)
    network.addColumns(sheet.ncols - 1)
    ui_mainwindow.tableWidget.recalc(network)
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            content = str(sheet.cell_value(i, j))
            network.getCell(i, j).input = content
            network.getCell(i, j).value = None if content == "" else content
            ui_mainwindow.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(content))
    network.title = file


def writter_csv(network, name):
    content = name + '.csv'
    sheet = csv.writer(open(content, 'w'))  # file name
    for x in range(0, len(network.matrix)):  # creation of the 'newfile', w as writting
        sheet.writerow([network.getCell(x, y).value for y in
                        range(0, len(network.matrix[x]))])  # writting of each row in comprehension
    print('saved')
    network.title = content


def reader_csv(file, ui_mainwindow, network):
    f = open(file)
    sheet = csv.reader(f)  # opening
    rows = len(f.readlines())
    f.seek(0)
    columns = len(next(sheet))
    f.seek(0)
    network.addRows(rows)
    network.addColumns(columns)
    network.title = file
    ui_mainwindow.tableWidget.recalc(network)
    i = 0
    for row in sheet:
        for j in range(0, len(row)):  # for each content or cell, a new QtWidget item is created
            content = row[j]
            network.getCell(i, j).input = content
            network.getCell(i, j).value = None if content == "" else content
            ui_mainwindow.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(content))
        i += 1
    print(network.getCellByName('B2').value)


def writter_marshalling(network, name):
    pickle.dump(network.matrix, open('{}.p'.format(name), 'wb'))
    print('saved')
    network.title = '{}.p'.format(name)
    network.saved=True


def reader_marshalling(file, ui_mainwindow, network):
    network.subsitute(pickle.load(open(file, 'rb')))
    ui_mainwindow.tableWidget.recalc(network)
    network.title = file


def extensionreader(a, ui_mainwindow, network):  # permet la lecture
    try:
        ui_mainwindow.indicator.setText("Ouverture en cours")
        chaine = a.split(os.extsep)
        key = chaine[1]
        if key == 'csv':
            reader_csv(a, ui_mainwindow, network)
            print('it is a csv file')
        elif key == 'xls':
            reader_xls(a, ui_mainwindow, network)
            print('it is a xls file')
        else:
            reader_marshalling(a, ui_mainwindow, network)
            print('it is a binary file')
        ui_mainwindow.indicator.setText("Ouvert")
        ui_mainwindow.retranslate(ui_mainwindow.Mainwindow)
        network.saved = True
    except IndexError:
        pass
    finally:
        print('open window closed')


def extensionwritter(a, network, ui_mainwindow):  # permet la lecture
    chaine = a.split(os.extsep)
    name = chaine[0]
    ui_mainwindow.indicator.setText("Sauvegarde en cours")
    try:
        key = chaine[1]
        if key == 'csv':
            writter_csv(network, name)
            print('it is a csv file')
        elif key == 'xls':
            writter_xls(network, name)
            print('it is a xls file')
        else:
            print("Can't open this file")
        ui_mainwindow.indicator.setText("Exporté")
        network.saved = True
        ui_mainwindow.retranslate(ui_mainwindow.Mainwindow)
    except IndexError:
        pass
    finally:
        print('save window closed')


def fileName(chaine):
    string = chaine.split(os.extsep)
    return string[0]
