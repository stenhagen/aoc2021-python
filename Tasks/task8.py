import Helpers.taskHelper as taskHelper
import re
import numpy as np
from functools import reduce

""" The input is a sequence of lines on the form:
gbcefa eac acfbg ae dcabfg begcdaf ecgba fgaedc beaf gcbde | cbgfa gedcb fgecab fbagdc

What comes before | is called the mapping schema.
What comes after | is called the output digits.

In part b a digit-segment-mapping is created. This is a dictionary
that maps a sequence of segment to the corresponding digit
for a row, i.e. a set of random segments. The sequence of segments
always come in alphabetical order. A non-random digit-segment-mapping
would therefore be:
{
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7
    'abcdefg': 8,
    'abcdfg': 9
}       


rules:
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
"""

"""
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
"""

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

segmentPattern = r'[a-g]{2,7}'

def printMatchesFormatted(matchList):
    """Debugging function used for printing """
    for line in matchList:
        print(",".join(line))

        """
        match len(line):
            case matches if matches == 0: pass 
            case matches if matches == 1:  print(line[0])
            case matches if matches > 1: 
                print(reduce(lambda m1, m2: m1 + "," + m2, line))   
        """

def calcNumberOfDigitsWithNSegments(valuesArray, n):
    """ Find all occurences of digits with n segments
    in list of output digit strings.
    """

    # Pattern contains negative lookahead expression (?!...) to only
    # match a sequence of segments if it's not followed directly by
    # a segment. 
    pattern = r'\s[a-g]{' + str(n) + r'}(?![a-g])'
    matches = sum([len(re.findall(pattern, v)) for v in valuesArray])
    return matches

def run8a():
    """ Counting the occurences of digits in the output that has a 
    unique number of segments, i.e. {1, 4, 7, 8}   
    """

    wiringSchema = taskHelper.readFile('Data/data8Help.txt')
    # Only extract the ouput digits
    actualValues = [
        valueSequence.split("|")[1] for valueSequence in wiringSchema
    ]
    digitsOfInterest = [1, 4, 7, 8]

    # Sum the occurences for all the digitsOfInterest   
    sumOfInterestingDigits = sum([
        calcNumberOfDigitsWithNSegments(actualValues, numberOfSegmentsDict[v])
        for v in digitsOfInterest
    ])
    print(sumOfInterestingDigits) 

def orderSegmentAlphabetically(digitUnorderedSegments):
    """ takes a digit with unordered segments and orders them:
    'facde' -> 'acdef'
    """
    listOfSegments = [seg for seg in digitUnorderedSegments]
    orderedListOfSegments = sorted(listOfSegments)
    digitOrderedSegments = ''.join(orderedListOfSegments)
    return digitOrderedSegments

def findSegmentMatches(source, target):
    """ Finds the number of segments that exist in source and target:
    Example:
    findSegmentMatches('acdf', 'afg') -> 2
    """
    return len([seg for seg in source if seg in target])

def findDigitSegmentMapping(mappingSchema):
    digitsInSchema = [
        orderSegmentAlphabetically(digit) 
        for digit in re.findall(segmentPattern, mappingSchema)
    ] 
    initial = -1
    digitSegmentMapping = dict.fromkeys(digitsInSchema, initial)
    
    # Pick out the digits with unique number of segments    
    for digit in digitSegmentMapping.keys():
        match len(digit):
            case i if i == numberOfSegmentsDict[1]:
                digitSegmentMapping[digit] = 1
            case i if i == numberOfSegmentsDict[4]:
                digitSegmentMapping[digit] = 4
            case i if i == numberOfSegmentsDict[7]:
                digitSegmentMapping[digit] = 7
            case i if i == numberOfSegmentsDict[8]:
                digitSegmentMapping[digit] = 8     

    # 2, 3, 5
    fiveSegmentDigits = [
        dig for dig in digitSegmentMapping.keys() if len(dig) == 5
    ]
    
    # 0, 6, 9
    sixSegmentDigits = [
        dig for dig in digitSegmentMapping.keys() if len(dig) == 6
    ]

    # Rule for 0: six segments, three segments from 7 and three segments
    # from 4 exists.
    zero = [
        dig for dig in sixSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 4)
        ) == 3 
        and findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 7)
        ) == 3
    ]
    taskHelper.assertSingleListItem(zero)
    digitSegmentMapping[zero[0]] = 0

    # Rule for 2: five segments and two from 4 exists
    two = [
        dig for dig in fiveSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 4)
        ) == 2
    ]
    taskHelper.assertSingleListItem(two)
    digitSegmentMapping[two[0]] = 2
    
    # Rule for 3: five segments and all two segments from 1 exists
    three = [
        dig for dig in fiveSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 1)
        ) == 2
    ]
    taskHelper.assertSingleListItem(three)
    digitSegmentMapping[three[0]] = 3 

    # Rule for 5: five segments, three from 4 and one segment from 1
    # exists 
    five = [
        dig for dig in fiveSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 4)
        ) == 3
        and findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 1)
        ) == 1
    ]
    taskHelper.assertSingleListItem(five)
    digitSegmentMapping[five[0]] = 5

    # Rule for 6: six segments, two segments from 7
    six = [
        dig for dig in sixSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 7)
        ) == 2
    ]
    taskHelper.assertSingleListItem(six)
    digitSegmentMapping[six[0]] = 6

    # Rule for 9: six segments, three segments from 7 and four segments
    # from 4
    nine = [
        dig for dig in sixSegmentDigits 
        if findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 4)
        ) == 4 
        and findSegmentMatches(
            dig, taskHelper.getKeyOfValue(digitSegmentMapping, 7)
        ) == 3
    ]
    taskHelper.assertSingleListItem(nine)
    digitSegmentMapping[nine[0]] = 9

    # Check that all numbers are mapped 
    try:
        if min(digitSegmentMapping.values()) < 0:
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Unmapped value exists")
        raise
    return digitSegmentMapping

def calculateOutputValue(digitSegmentMapping, outputDigitsUnordered):
    """ Calculate the output value from a string of output values with
    unordered segments with help of digitSegmentMapping.
    """

    digitsInOutput = [
        orderSegmentAlphabetically(digit) 
        for digit in re.findall(segmentPattern, outputDigitsUnordered)
    ]
    outputValue = int(
        "".join([str(digitSegmentMapping[dig]) 
        for dig in digitsInOutput])
    )
    return outputValue

def calculateOutputValueForLine(line):
    """ Calculates the ouput value given a line consisting of a 
    mapping schema and output digits. 
    If the output digits are: (1, 4, 6, 8) then the output value is 
    1468. 
    """
    lineSplitted = line.split("|")
    mappingSchema = lineSplitted[0]
    outputDigits = lineSplitted[1]

    digitSegmentMapping = findDigitSegmentMapping(mappingSchema)
    outputValue = calculateOutputValue(digitSegmentMapping, outputDigits)
    return outputValue

def run8b():
    lines = taskHelper.readFile('Data/data8.txt') 
    outputValues = [calculateOutputValueForLine(line) for line in lines] 
    finalSum = sum(outputValues)
    print(finalSum)