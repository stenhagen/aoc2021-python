import Helpers.taskHelper as taskHelper
import numpy as np

def createLine(lineString):
    coordinatePair = [[int(c) for c in pair.strip().split(',')] for pair in lineString.split('->')]
    return np.expand_dims(np.array(coordinatePair), axis = 2)

def initializeDiagram(pairs):
    max_x = np.amax(pairs[:,0,:])
    max_y = np.amax(pairs[:,1,:])
    return np.zeros((max_y + 1, max_x + 1), dtype = int)

def addOneDimLine(diagram, pair):
    try:
        if (pair[0,0] == pair[1,0]):
            xChanging = False
            isGrowing = taskHelper.numpyBoolToBool(pair[0,1] < pair[1,1]) 
        elif (pair[0,1] == pair[1,1]):
            xChanging = True
            isGrowing = taskHelper.numpyBoolToBool(pair[0,0] < pair[1,0]) 
        else:
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Lines must be either vertical or hoizontal")
        raise

    match (xChanging, isGrowing):
        case (True, True): diagram[pair[0,1], pair[0,0] : pair[1,0] + 1] = diagram[pair[0,1], pair[0,0] : pair[1,0] + 1] + 1  
        case (True, False): diagram[pair[0,1], pair[1,0] : pair[0,0] + 1] = diagram[pair[0,1], pair[1,0] : pair[0,0] + 1] + 1
        case (False, True): diagram[pair[0,1] : pair[1,1] + 1, pair[0,0]] = diagram[pair[0,1] : pair[1,1] + 1, pair[0,0]] + 1
        case (False, False): diagram[pair[1,1] : pair[0,1] + 1, pair[0,0]] = diagram[pair[1,1] : pair[0,1] + 1, pair[0,0]] + 1
    return diagram   

def addDiagonalLine(diagram, pair):
    try:
        if abs(pair[0,0] - pair[1,0]) != abs(pair[0,1] - pair[1,1]):
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Non One-dimensional lines must be completely diagonal")
        raise

    xGrowing = taskHelper.numpyBoolToBool(pair[0,0] < pair[1,0])
    yGrowing = taskHelper.numpyBoolToBool(pair[0,1] < pair[1,1])

    match (xGrowing, yGrowing):
        case (True, True):
            xValues = range(pair[0,0], pair[1,0] + 1)
            yValues = range(pair[0,1], pair[1,1] + 1)
        case (True, False):
            xValues = range(pair[0,0], pair[1,0] + 1)
            yValues = range(pair[0,1], pair[1,1] - 1, -1)    
        case (False, True):
            xValues = range(pair[0,0], pair[1,0] - 1, -1)
            yValues = range(pair[0,1], pair[1,1] + 1)    
        case (False, False):
            xValues = range(pair[0,0], pair[1,0] - 1, -1)
            yValues = range(pair[0,1], pair[1,1] - 1, -1)    
        
    coords = zip(xValues, yValues)
    for coord in coords:
        diagram[coord[1], coord[0]] = diagram[coord[1], coord[0]] + 1 
    
    return diagram

def addLine(diagram, pair):
    pairShape = pair.shape
    if len(pairShape) > 2:
        try:
            if pairShape[2] > 1:
                raise(taskHelper.Exc)
            else:
                pair2d = np.squeeze(pair, axis = 2)
        except taskHelper.Exc:
            print("The pair must be 2-dimensional or have only a single third dimension")
            raise
    else:
        pair2d = pair
    
    if pair2d[0,0] == pair2d[1,0] or pair2d[0,1] == pair2d[1,1]: 
        return addOneDimLine(diagram, pair2d)
    else: 
        return addDiagonalLine(diagram, pair2d)

def numberOfDangerPoints(diagram, dangerLimit):
    return len(np.where(diagram >= dangerLimit)[0])  

def run5a():
    lines = taskHelper.readFile('Data\\data5.txt')
    linePairs = [createLine(l) for l in lines]
    oneDimFiltered = [pair for pair in linePairs if pair[0,0,0] == pair[1,0,0] or pair[0,1,0] == pair[1,1,0]]
    pairsArray = oneDimFiltered[0]
    for p in oneDimFiltered[1:]:
        pairsArray = np.append(pairsArray, p, axis = 2)

    diagram = initializeDiagram(pairsArray)
    for lineIndex in range(np.shape(pairsArray)[2]):
        diagram = addLine(diagram, pairsArray[:,:,lineIndex])

    print(numberOfDangerPoints(diagram, 2))

def run5b():
    lines = taskHelper.readFile('Data\\data5.txt')
    linePairs = [createLine(l) for l in lines]
    pairsArray = linePairs[0]
    for p in linePairs[1:]:
        pairsArray = np.append(pairsArray, p, axis = 2)

    diagram = initializeDiagram(pairsArray)
    for lineIndex in range(np.shape(pairsArray)[2]):
        diagram = addLine(diagram, pairsArray[:,:,lineIndex])

    print(numberOfDangerPoints(diagram, 2))
    


    