from math import gamma
import Helpers.taskHelper as taskHelper
import re

def flipBit(b):
    return '1' if b == '0' else '0'

def run3a():
    codes = taskHelper.readFile('Data/data3.txt')
    codeLength = len(codes[0])
    gammaString = ''
    for pos in range(0, codeLength - 1):
        ones = 0
        zeros = 0
        for code in codes:
            match code[pos]:
                case '0': zeros += 1
                case '1': ones += 1
        gammaString = gammaString + '0' if zeros > ones else gammaString + '1'
    epsilonString = ''.join(flipBit(b) for b in gammaString)
    gammaDecimal = int(gammaString, 2)
    epsilonDecimal = int(epsilonString, 2)
    print(gammaDecimal * epsilonDecimal)

def filterCodesForBit(codes, bitPosition, searchMostCommon, bitIfTied):
    bitListForPosition = list(map(lambda code: int(code[bitPosition]), codes))
    numberOfCodes = len(codes)
    bitSum = sum(bitListForPosition)
    percentageOfOnes = bitSum/numberOfCodes
    if percentageOfOnes < 0.5:
        bitToSelect = '0' if searchMostCommon else '1'
    elif percentageOfOnes > 0.5:
        bitToSelect = '1' if searchMostCommon else '0'
    elif percentageOfOnes == 0.5:
        bitToSelect = bitIfTied
    return list(filter(lambda code: code[bitPosition] == bitToSelect, codes))


def run3b():
    codes = taskHelper.readFile('Data/data3.txt')
    codeLength = len(codes[0])
    oxygenCodes = codes
    for pos in range(0, codeLength - 1):
        oxygenCodes = filterCodesForBit(oxygenCodes, pos, True, '1')
        if len(oxygenCodes) == 1:
            break
    
    co2Codes = codes
    for pos in range(0, codeLength - 1):
        co2Codes = filterCodesForBit(co2Codes, pos, False, '0')
        if len(co2Codes) == 1:
            break
    
    if len(oxygenCodes) > 1 or len(co2Codes) > 1: print("Unable to determine single code")
    result = int(oxygenCodes[0], 2) * int(co2Codes[0], 2)
    print(result) 
    