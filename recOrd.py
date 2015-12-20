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


def reader_xls(file):

    #opening of the file as a binder
    binder=xlrd.open_workbook(file)
    #listing of sheet names
    sheets=binder.sheet_names()
    #recovering of the i eme sheet
    sheet=binder.sheet_by_name(sheets[0])
    #display the sheet but where find it

def writter_csv(network):
     #file name
    sheet=csv.writer(open('newfile.csv','w'))
    #creation of the 'newfile', w as writting
    for x in range(0,len(network.matrix)):
        sheet.writerow([network.getCell(x,y).input for y in range(0,len(network.matrix[x]))])
        #writting of each row in comprehension

# def reader_csv(file):
#     from main import ui_mainwindow, traitement
#     sheet=csv.reader(open(file))
#     i=0
#     j=0
#     for row in sheet :
#         i+=1
#         for j  in range(0,len(row)):
#             j+=1
#             item= QtWidgets.QTableWidgetItem()
#             ui_mainwindow.tableWidget.setItem(i,j,item)
#             content=row[j-1]
#             traitement(i,j,content)
#             print(i,j)

#le marshalling n est pas encore pret...ne le testez pas sinon....

def writter_marshalling(network):
    marshal.dump([[network.getCell(x,y).input for y in range(0,len(network.matrix[x]))]
                  for x in range(0,len(network.matrix))],open('marshalling.pyc','wb'))
    #witting in coprehension of the file, we have to transform each cell in string

def reader_marshalling():
    a=input('entrer un fichier')
    file=open(a,'r')
    marshal.loads(file)

#reader_marshalling()