import xlrd
from xlwt import Workbook
import csv as csv
import marshal


def binder(network):
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

def read(file,i):
    #opening of the file as a binder
    binder=xlrd.open_workbook(file)
    #listing of sheet names
    sheets=binder.sheet_names()
    #recovering of the i eme sheet
    sheet=binder.sheet_by_name(sheets[i])
    sheet.view()
    #display the sheet but where find it?

def binder2(network):
     #file name
    sheet=csv.writer(open('newfile.csv','w'))
    #creation of the 'newfile', w as writting
    for x in range(0,len(network.matrix)):
        sheet.writerow([network.getCell(x,y).input for y in range(0,len(network.matrix[x]))])
        #writting of each row in comprehension

def read2(file):
    a=input()
    sheet=csv.reader(open(a))
    #opening
    for row in sheet:
        print(row)
    #view
#le marshalling n est pas encore pret...ne le testez pas sinon....
def binder3(network):
    marshal.dump([[network.getCell(x,y).input for y in range(0,len(network.matrix[x]))]
                  for x in range(0,len(network.matrix))],open('marshalling.pyc','wb'))
    #witting in coprehension of the file, we have to transform each cell in string

def read3():
    a=input('entrer un fichier')
    file=open(a)
    marshal.loads(file)