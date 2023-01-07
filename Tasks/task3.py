from math import gamma
import Helpers.taskHelper as taskHelper
import re

def flipBit(b):
    return '1' if b == '0' else '0'

def run3a():
    """Solved by going through each row and incrementing bit count.
    Should be solved by creating a numpy matrix and summing along the 
    correct axis       
    """
    
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
    
    # Epsilon rate can be found through flip of the gamma rate since 
    # it's the least common bit per position rather than the most common,
    epsilonString = ''.join(flipBit(b) for b in gammaString)
    gammaDecimal = int(gammaString, 2)
    epsilonDecimal = int(epsilonString, 2)
    print(gammaDecimal * epsilonDecimal)


def filterCodesForBit(codes, bitPosition, searchMostCommon, bitIfTied):
    """ Function that filters a set of input codes to an output 
    set of codes given the bitPosition and search rules.
    """

    # Create list of bits across codes for the relevant bit position.  
    bitListForPosition = list(map(lambda code: int(code[bitPosition]), codes))
    
    # Determine if the position should be 0 or 1  
    numberOfCodes = len(codes)
    bitSum = sum(bitListForPosition)
    percentageOfOnes = bitSum/numberOfCodes
    if percentageOfOnes < 0.5:
        bitToSelect = '0' if searchMostCommon else '1'
    elif percentageOfOnes > 0.5:
        bitToSelect = '1' if searchMostCommon else '0'
    elif percentageOfOnes == 0.5:
        bitToSelect = bitIfTied
    
    # Rerurn all codes that matches the required bit.  
    return list(filter(lambda code: code[bitPosition] == bitToSelect, codes))


def run3b():
    """ Search through set of codes and filter it down for the oxygen
    and the co2 criterias separately. 
    """
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
    