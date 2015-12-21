import xlrd
from xlwt import Workbook
import csv as csv
import marshal
from PyQt5 import QtWidgets
import os
def writter_xls(network):
    binder=Workbook()   #creation of the binder
    sheet= binder.add_sheet('page') #creation of the sheet
    for x in range(0,len(network.matrix)):             #writting of each cell
        for y in range(0,len(network.matrix[x])):
            sheet.write(y,x,network.getCell(x,y).value)
            print(network.getCell(x,y).value)
    binder.save('test.xls') #save file
    print('file saved')

def reader_xls(file,ui_mainwindow,traitement):
    binder=xlrd.open_workbook(file) #opening of the file as a binder
    sheets=binder.sheet_names() #listing of sheet names
    sheet=binder.sheet_by_name(sheets[0]) #recovering of the i eme sheet
    for i in range(1,sheet.nrows):
        for j in range(1,sheet.ncols):
         content=sheet.cell_value(i,j)
         item= QtWidgets.QTableWidgetItem()
         ui_mainwindow.tableWidget.setItem(i-1,j-1,item)
         traitement(i-1,j-1,content)

def writter_csv(network):
    sheet=csv.writer(open('newfile.csv','w'))      #file name
    for x in range(0,len(network.matrix)):        #creation of the 'newfile', w as writting
        sheet.writerow([network.getCell(x,y).input for y in range(0,len(network.matrix[x]))])        #writting of each row in comprehension
    print('saved')

def reader_csv(file,ui_mainwindow,traitement):
    sheet=csv.reader(open(file)) #opening
    i=0
    for row in sheet :
        i+=1
        for j  in range(0,len(row)):  #for each content or cell, a new QtWidget item is created
            j+=1
            item= QtWidgets.QTableWidgetItem()
            ui_mainwindow.tableWidget.setItem(i-1,j-1,item)
            content=row[j-1]
            traitement(i-1,j-1,content)

def writter_marshalling(network):
    marshal.dump([[network.getCell(x,y).input for y in range(0,len(network.matrix[x]))]
                  for x in range(0,len(network.matrix))],open('marshalling.pyc','wb'))
    print('saved')

def reader_marshalling(file,ui_mainwindow,traitement):
    data=marshal.load(open(file,'rb')) #opening
    i=0
    for row in data:
        i+=1
        for j  in range(0,len(row)):# as for csv
            j+=1
            item= QtWidgets.QTableWidgetItem()
            ui_mainwindow.tableWidget.setItem(i-1,j-1,item)
            content=row[j-1]
            traitement(i-1,j-1,content)

# def extension(a,ui_mainwindow,traitement):
#
#     try:
#         if str(a[0]).split(os.extsep)==csv:
#             reader_csv(a,ui_mainwindow,traitement)
#         elif str(a[0]).split(os.extsep)==xls:
#             reader_xls(a,ui_mainwindow,traitement)
#         else:
#             reader_marshalling(a,ui_mainwindow,traitement)
#     except:
#         print('extension error')


