#Un type de fonction est ici definie par son nom (String) et son evaluation (String) en une liste d'arguments args
#Exemple: -Function('carre','args[0]**2') correspond à la fonction carré
#         -Function('Moyenne','sum(args)/len(args)') correspond à la fonction moyenne
#Elles sont répertoriées dans un objet de type Knownfunctions

class Function():
    def __init__(self,name,output):
        self.name=name
        self.output=output

    def value(self,args):
        try:
            return eval(self.output)
        except IndexError:
            return 'Index Error'
        except:
            return 'Invalid Syntax'

class Knownfunctions():
    def __init__(self):
        self.dict={}

    def add(self,function):
        self.dict[function.name]=function
