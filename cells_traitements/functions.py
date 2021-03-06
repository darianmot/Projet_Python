"""Un type de fonction est ici definie par son nom (String) et son evaluation (String) en une liste d'arguments args
Exemple: -Function('carre','args[0]**2') correspond à la fonction carré
        -Function('Moyenne','sum(args)/len(args)') correspond à la fonction moyenne
Elles sont répertoriées dans un objet de type Knownfunctions"""

import math, statistics as stat, time, random

# Définie l'objet représentant une fonction
class Function():
    def __init__(self, name, output, description, category):
        self.name = name
        self.output = output
        self.description = description
        self.category = category

    def value(self, args):
        try:
            return eval(self.output.replace('args',str(args)))
        except IndexError:
            return '#Index Error'
        except Exception as e:
            return '#Error : {}'.format(e)

    def __repr__(self):
        return self.name + ' : ' + self.output

# Classe (ou dictionnaire) contenant les fonctions rentré par l'utilisateur
class Knownfunctions():
    def __init__(self):
        self.dict = {}
        self.category = []

    def addFun(self, function):
        self.dict[function.name] = function

    def removeFun(self, function):
        del self.dict[function.name]

    def getFunction(self, name):
        try:
            return self.dict.get(name)
        except:
            return 0

    def getFunList(self):
        l = []
        for fun in self.dict.values():
            l.append(fun)
        return sorted(l, key=lambda x: x.name)

    def addCategory(self, string):
        self.category.append(string)

    def delCategory(self, string):
        self.category.remove(string)

    def getCategoryList(self):
        categories = [category for category in self.category if category != "Other"]
        return sorted(categories) + ["Other"]

    def functionOfCategory(self, string):
        l = []
        for fun in self.dict.values():
            if fun.category == string:
                l.append(fun)
        return sorted(l, key=lambda x: x.name)

    def isFunValid(self, name, evaluation, isfunction):
        if len(name) == 0 or len(evaluation) == 0 or (
        not isfunction(name)) or name in self.dict.keys() or name == 'args':
            return False
        return True

    def __repr__(self):
        return str(self.dict)
