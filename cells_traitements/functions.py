#Un type de fonction est ici definie par son nom (String) et son evaluation (String) en une liste d'arguments args
#Exemple: -Function('carre','args[0]**2') correspond à la fonction carré
#         -Function('Moyenne','sum(args)/len(args)') correspond à la fonction moyenne
#Elles sont répertoriées dans un objet de type Knownfunctions
import math
class Function():
    def __init__(self,name,output, description,category):
        self.name=name
        self.output=output
        self.description=description
        self.category=category

    def value(self,args):
        try:
            return eval(self.output)
        except IndexError:
            return '#Index Error'
        except Exception as e:
            return '#Error : {}'.format(e)
    def __repr__(self):
        return self.name+' : '+self.output

class Knownfunctions():
    def __init__(self):
        self.dict={}
        self.category=[]
        self.initialize()

    def addFun(self,function):
        self.dict[function.name]=function

    def removeFun(self,function):
        del self.dict[function.name]

    def getFunction(self,name):
        try:
            return self.dict.get(name)
        except:
            return 0

    def getFunList(self):
        l=[]
        for fun in self.dict.values():
            l.append(fun)
        return sorted(l,key=lambda x:x.name)

    def addCategory(self,string):
        self.category.append(string)

    def getCategoryList(self):
        return sorted(self.category)

    def functionOfCategory(self,string):
        l=[]
        for fun in self.dict.values():
            if fun.category==string:
                l.append(fun)
        return sorted(l,key=lambda x:x.name)

    def isFunValid(self,name,evaluation):
        if len(name)==0 or len(evaluation)==0:
            return False
        if not(name.isalpha()):
            return False
        if name in self.dict.keys() or name=='args':
            return False
        return True

    def initialize(self):
        self.addCategory('All')
        self.addCategory('Math')
        self.addCategory('Stat')
        self.addFun(Function('average','sum(args)/len(args)', 'Retourne la moyenne des cellules selectionnées.','Stat'))
        self.addFun(Function('sum','sum(args)', 'Retourne la somme des cellules selectionnées.','Math'))
        self.addFun(Function('cos','math.cos(args[0])', 'Retourne le cosinus de la celulle selectionnée','Math'))
        self.addFun(Function('exp','math.exp(args[0])', 'Retourne le exp', 'Math'))

    def __repr__(self):
        return str(self.dict)
