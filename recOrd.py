import xlrd
from xlwt import Workbook
import csv as csv
import marshal
from PyQt5 import QtWidgets

from structures import Cell

def writter_xls(network):

    #creation of the binder
    binder=Workbook()
    #creation of the sheet
    sheet= binder.add_sheet('page')
    #writting of each cell
    for x in range(0,len(network.matrix)):
        for y in range(0,len(network.matrix[x])):
            sheet.write(y,x,network.getCell(x,y).value)
            print(network.getCell(x,y).value)
    #save file
    binder.save('test.xls')
    print('file saved')
#
# import win32com.client as win32
# from win32com.client import Dispatch
#
# path = os.path.join("C:\\", "Users","*****","Desktop","test.xls")
# #Lance le processus Excel
# xlApp = Dispatch("Excel.Application")
# #Excel une fois lancé s'affiche (à false il s'execute en tache de fond on ne le voit pas)
# xlApp.Visible=True
# #Ouverture du fichier
# xlWb = xlApp.Workbooks.Open(path)
# #Affichage de la cellule C1 (coordonnées 1,3 ligne colonne)
# print ("C1:",xlWb.ActiveSheet.Cells(1,3).Value)

def reader_xls(file):
    from main import ui_mainwindow, traitement
    #opening of the file as a binder
    binder=xlrd.open_workbook(file)
    #listing of sheet names
    sheets=binder.sheet_names()
    #recovering of the i eme sheet
    sheet=binder.sheet_by_name(sheets[0])
    #display the sheet but where find it

    for i in range(1,sheet.nrows):
        for j in range(1,sheet.ncols):
         content=sheet.cell_value(i,j)
         item= QtWidgets.QTableWidgetItem()
         ui_mainwindow.tableWidget.setItem(i,j,item)
         traitement(i,j,content)

def writter_csv(network):
     #file name
    sheet=csv.writer(open('newfile.csv','w'))
    #creation of the 'newfile', w as writting
    for x in range(0,len(network.matrix)):
        sheet.writerow([network.getCell(x,y).input for y in range(0,len(network.matrix[x]))])
        #writting of each row in comprehension

def reader_csv(file):
    from main import ui_mainwindow, traitement
    sheet=csv.reader(open(file))
    i=0
    j=0
    for row in sheet :
        i+=1
        for j  in range(0,len(row)):
            j+=1
            item= QtWidgets.QTableWidgetItem()
            ui_mainwindow.tableWidget.setItem(i,j,item)
            content=row[j-1]
            traitement(i,j,content)

#le marshalling n est pas encore pret...ne le testez pas sinon....

def writter_marshalling(network):
    marshal.dump([[network.getCell(x,y).input for y in range(0,len(network.matrix[x]))]
                  for x in range(0,len(network.matrix))],open('marshalling.pyc','wb'))
    print('saved')


def reader_marshalling(file):
    from main import ui_mainwindow, traitement
    data=marshal.load(open(file,'rb'))
    i=0
    j=0
    for row in data:
        i+=1
        for j  in range(0,len(row)):
            j+=1
            item= QtWidgets.QTableWidgetItem()
            ui_mainwindow.tableWidget.setItem(i,j,item)
            content=row[j-1]
            traitement(i,j,content)



