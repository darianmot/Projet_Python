#Un type de fonction est ici definie par son nom (String) et son evaluation (String) en une liste d'arguments args
#Exemple: -Function('carre','args[0]**2') correspond à la fonction carré
#         -Function('Moyenne','sum(args)/len(args)') correspond à la fonction moyenne
#Elles sont répertoriées dans un objet de type Knownfunctions
import math
class Function():
    def __init__(self,name,output, description):
        self.name=name
        self.output=output
        self.description=description

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
        self.initialize()

    def add(self,function):
        self.dict[function.name]=function

    def initialize(self):
        self.add(Function('average','sum(args)/len(args)', 'Retourne la moyenne des cellules selectionnées.'))
        self.add(Function('sum','sum(args)', 'Retourne la somme des cellules selectionnées.'))
        self.add(Function('cos','math.cos(args[0])', 'Retourne le cosinus de la celulle selectionnée'))

    def getFunction(self,name):
        try:
            return self.dict.get(name)
        except:
            return 0

    def getList(self):
        l=[]
        for fun in self.dict.values():
            l.append(fun)
        return sorted(l,key=lambda x:x.name)

    def __repr__(self):
        return str(self.dict)
