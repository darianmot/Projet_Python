import xlrd, csv
from xlwt import Workbook
import structures
import pickle
from PyQt5 import QtWidgets
import os


def writter_xls(network, name):
    content = name + '.xls'
    binder = Workbook()  # creation of the binder
    sheet = binder.add_sheet('page')  # creation of the sheet
    for x in range(0, len(network.matrix[0])):  # writting of each cell
        for y in range(0, len(network.matrix)):
            sheet.write(y, x, network.getCell(y, x).value)
    binder.save(content)  # save file
    print('file saved')


def reader_xls(file, ui_mainwindow, network):
    binder = xlrd.open_workbook(file)  # opening of the file as a binder
    sheets = binder.sheet_names()  # listing of sheet names
    sheet = binder.sheet_by_name(sheets[0])  # recovering of the i eme sheet
    network.reset(1,1)
    network.addRows(sheet.nrows-1)
    network.addColumns(sheet.ncols-1)
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            content=str(sheet.cell_value(i,j))
            network.getCell(i,j).input = content
            network.getCell(i,j).value = content
            ui_mainwindow.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(content))

def writter_csv(network, name):
    content = name + '.csv'
    sheet = csv.writer(open(content, 'w'))  # file name
    for x in range(0, len(network.matrix)):  # creation of the 'newfile', w as writting
        sheet.writerow([network.getCell(x, y).value for y in
                        range(0, len(network.matrix[x]))])  # writting of each row in comprehension
    print('saved')


def reader_csv(file, ui_mainwindow, traitement):
    sheet = csv.reader(open(file))  # opening
    i = 0
    for row in sheet:
        i += 1
        for j in range(0, len(row)):  # for each content or cell, a new QtWidget item is created
            j += 1
            content = row[j - 1]
            item = QtWidgets.QTableWidgetItem(content)
            ui_mainwindow.tableWidget.setItem(i - 1, j - 1, item)
            traitement(i - 1, j - 1, content)


def writter_marshalling(network, name):
    pickle.dump(network.matrix,open('{}.p'.format(name),'wb'))
    print('saved')


def reader_marshalling(file, ui_mainwindow, traitement,network):
    network.subsitute(pickle.load(open(file, 'rb')))  # opening
    ui_mainwindow.tableWidget.recalc(network)


def extensionreader(a, ui_mainwindow, traitement,network):  # permet la lecture
    try:
        ui_mainwindow.indicator.setText("Ouverture en cours")
        chaine = a.split(os.extsep)
        key = chaine[1]
        if key == 'csv':
            reader_csv(a, ui_mainwindow, traitement)
            print('it is a csv file')
        elif key == 'xls':
            reader_xls(a, ui_mainwindow, network)
            print('it is a xls file')
        else:
            reader_marshalling(a, ui_mainwindow, traitement, network)
            print('it is a binary file')
        ui_mainwindow.indicator.setText("Ouvert")
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
            writter_marshalling(network, name)
            print('it is a binary file')
        ui_mainwindow.indicator.setText("Sauvegardé")
    except IndexError:
        pass
    finally:
        print('save window closed')
