import os 
import numpy as np

class Exc(Exception):
    pass

def getProjectRoot():
    fileRoot = os.path.dirname(os.path.abspath(__file__))
    projectDir = 'aoc2021-python'
    pathLength = fileRoot.find(projectDir) + len(projectDir)  # The start of ProjectDir + lengt of projectDir
    projectRoot = fileRoot[0:pathLength] + '\\'
    return projectRoot

def readFile(pathInProject): 
    projectRoot = getProjectRoot()
    with open(os.path.join(projectRoot, pathInProject)) as f:
        lines = f.readlines()
    return lines

def numpyBoolToBool(numpyBool):
    match numpyBool:
        case np.True_: return True
        case np.False_: return False