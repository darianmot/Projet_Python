import cells_traitements.decomposition as decomposition, cells_traitements.tritopologique as tritopologique
import time


# Renvoie l'évaluation d'une formule, au sein d'un réseau nétwork (ou affiche l'erreur le cas écheant)
def chainEvaluation(network, chaine, knownFunctions, stringDict):
    (elementList, elementType) = decomposition.decompo(chaine)
    i = 0
    decomposition.doublePoint(elementList, elementType, network)
    while i < len(elementList):
        if elementType[i] == 'cell':
            try:
                elementList[i] = str(network.getCellByName(elementList[i]).value)
            except decomposition.Error as e:
                raise decomposition.Error(e.reason)
        elif elementType[i] == 'function' and elementList[i] not in stringDict:
            try:
                value = eval_function(network, elementList, elementType, i, knownFunctions)
            except decomposition.Error as e:
                raise decomposition.Error(e.reason)
            if decomposition.isError(str(value)):
                return value
            end = decomposition.endOfFunction(elementList, i)
            elementList[i:end + 1] = [str(value)]
            elementType[i:end + 1] = ['nombre']
        i += 1
    try:
        return eval(''.join(elementList), None, stringDict)
    except SyntaxError as e:
        print("Error de syntaxe: {}".format(elementList))
        raise decomposition.Error('Syntaxe ({})'.format(e.msg))
    except ZeroDivisionError:
        raise decomposition.Error('Division par 0')
    except NameError as e:
        stringDict[str(e).split("'")[1]] = str(e).split("'")[1]
        return chainEvaluation(network, ''.join(elementList), knownFunctions, stringDict)
    except Exception as e:
        print("Can't evaluate '{0}'".format(''.join(elementList)), end='')
        raise decomposition.Error(str(e))


# Renvoie l'évaluation d'une fonction en position k dans une liste d'element.
def eval_function(network, elementList, elementType, k, knownFunctions):
    element = elementList[k]
    if element not in knownFunctions.dict:  # Si la fonction n'est pas connue, on renvoie une erreur
        raise decomposition.Error('{} n\'est pas connue'.format(elementList[k]))
    try:
        if elementType[k + 1] != 'p_ouvrante':
            raise decomposition.Error('\'(\' attendue après {}'.format(elementList[k]))
    except IndexError:
        raise decomposition.Error('\'()\' attendue après {}'.format(elementList[k]))
    p_count = 1  # Pour verifier le parenthesage
    args = []
    currentArg = ""
    k += 2
    while p_count > 0 and k < len(elementList):
        if elementType[k] == 'function':  # Si c'est une fonction, on l'évalue recursivement
            value = eval_function(network, elementList, elementType, k, knownFunctions)
            if decomposition.isError(str(value)):
                return value
            k = decomposition.endOfFunction(elementList, k)
            args.append(value)
            currentArg = ""
        elif elementType[k] == 'sep':
            if currentArg != "":  # S'il n'y a rien avant un separateur, la syntaxe n'est pas correcte
                args.append(chainEvaluation(network, currentArg, knownFunctions, {}))
                currentArg = ""
        elif elementType[k] == 'p_fermante':  # On gère le parenthesage
            p_count -= 1
            if p_count > 0:
                currentArg += elementList[k]
        elif elementType[k] == 'p_ouvrante':
            p_count += 1
            currentArg += elementList[k]
        else:
            currentArg += elementList[k]
        k += 1
    if p_count != 0:
        raise decomposition.Error('parenthesage incorrect')
    if currentArg != "":
        args.append(chainEvaluation(network, currentArg, knownFunctions, {}))
    return knownFunctions.dict[str(element)].value(args)


# Traitement de l'input d'une celulle
def cellEvaluation(x, y, string, network, ui_mainwindow, knownFunctions):
    cell = network.getCell(x, y)
    cell.input = string
    cell.updateParents(network)
    t_init = time.time()
    if len(string) > 0:
        print('Evaluation de {0} et de ses cellules filles ... '.format(cell.name, len(cell.children_cells)), end='')
        ui_mainwindow.indicator.setText(
                'Evaluation de {0} et de ses cellules filles ... '.format(cell.name, len(cell.children_cells)))
        try:
            if string[0] == '=':
                for parentCell in cell.parent_cells:
                    if parentCell.name == cell.name:
                        raise decomposition.Error('Dépendance récursive de la celulle {}'.format(cell.name))
                cell.value = str(chainEvaluation(network, string[1:], knownFunctions, {}))
            else:
                cell.value = string
            try:
                order = tritopologique.evalOrder(cell)
                for child in order:
                    child.value = str(chainEvaluation(network, child.input[1:], knownFunctions, {}))
                    ui_mainwindow.tableWidget.return_value.emit(child.x, child.y, child.value)
            except decomposition.Error as e:
                for child in tritopologique.childrenCellsRec(cell)[1:]:
                    network.getCell(child.x, child.y).value = e.disp
                    ui_mainwindow.tableWidget.return_value.emit(child.x, child.y, e.disp)
            except tritopologique.CycleError:
                raise decomposition.Error("Dépendance cyclique")
            ui_mainwindow.tableWidget.return_value.emit(x, y, str(cell.value))
        except decomposition.Error as e:
            for child in tritopologique.childrenCellsRec(cell):
                network.getCell(child.x, child.y).value = e.disp
                ui_mainwindow.tableWidget.return_value.emit(child.x, child.y, e.disp)
        t_end = time.time()
        print('Done : ({}s)'.format(t_end - t_init))
        ui_mainwindow.indicator.setText(ui_mainwindow.indicator.text() + 'Done : ({}s)'.format(t_end - t_init))
    else:
        cell.value = None
        ui_mainwindow.tableWidget.takeItem(x, y)
        order = tritopologique.evalOrder(cell)
        for child in order:
            ui_mainwindow.tableWidget.return_value.emit(child.x, child.y,
                                                        "#Error : la cellule {} est vide".format(cell.name))
