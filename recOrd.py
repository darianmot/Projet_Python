import xlrd
from xlwt import Workbook

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
