import Helpers.taskHelper as taskHelper
import re
import numpy as np

numberOfSegmentsDict = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}

digitSegmentMapping = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'}
}

def calcNumberOfDigitsWithNSegments(valuesArray, n):
    pattern = r'\s[a-g]{' + str(n) + r'}(?![a-g])' 
    matches = sum([len(re.findall(pattern, v)) for v in valuesArray])
    return matches

def run8a():
    wiringSchema = taskHelper.readFile('Datadata8.txt')
    actualValues = [valueSequence.split("|")[1] for valueSequence in wiringSchema]
    digitsOfInterest = [1, 4, 7, 8] # According to input
    sumOfInterestingDigits = sum([calcNumberOfDigitsWithNSegments(actualValues, numberOfSegmentsDict[v]) for v in digitsOfInterest])
    print(sumOfInterestingDigits) 
        
def run8b():
    wiringSchema = taskHelper.readFile('Datadata8.txt')
    mappingSchema = [valueSequence.split("|")[0] for valueSequence in wiringSchema]
    actualValues = [valueSequence.split("|")[1] for valueSequence in wiringSchema]
    digitPattern = r'[a-g]{2,7}'
    

    #rules:
    # 0: 6 digits, missing one from 4 OK
    # 1: 2 digits OK
    # 2: 5 digits, not fully exists in 6 OK
    # 3: 5 digits, all from 1 exists OK
    # 4: 4 digits OK
    # 5: 5 digits, fully exists in 6 OK
    # 6: 6 digits, missing one of the two digits from 1 OK
    # 7: 3 digits OK
    # 8: 7 digits OK
    # 9: 6 digits, all from 4 exists OK