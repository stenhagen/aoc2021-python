import os 
import numpy as np

class Exc(Exception):
    pass

def getProjectRoot():
    fileRoot = os.path.dirname(os.path.abspath(__file__))
    projectDir = 'aoc2021-python'
    
    # The start of ProjectDir + length of projectDir
    pathLength = fileRoot.find(projectDir) + len(projectDir)  
    projectRoot = fileRoot[0:pathLength]
    return projectRoot

def readFile(pathInProject): 
    """Returns file context as a list of string with one line in 
    original file per list item.
    """
    
    projectRoot = getProjectRoot()
    with open(os.path.join(projectRoot, pathInProject)) as f:
        lines = f.readlines()
    return lines

def numpyBoolToBool(numpyBool):
    """ If making comparsions between numpy elements you'll get a 
    numpy bool. These are not nice.
    """
    match numpyBool:
        case np.True_: return True
        case np.False_: return False

def getKeyOfValue(d, v):
    """Do reverse search in dictionary.
    Fails if there is more than one key for value
    """
    key = [k for k in d.keys() if d[k] == v]
    try:
        if len(key) < 1:
            raise(Exc)
    except Exc:
        print("No key match for value = {value} in dictionary".format(value = v))
        raise

    try:
        if len(key) > 1:
            raise(Exc)
    except Exc:
        print("Multiple key matches for value = {value} in dictionary".format(value = v))
        raise

    return key[0]

def assertSingleListItem(list):
    try:
        if len(list) != 1:
            raise(Exc)
    except Exc:
        print("List contains no or multiple values")
        raise