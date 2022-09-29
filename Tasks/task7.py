import Helpers.taskHelper as taskHelper
import re
import numpy as np


def calculateFuel(orignalPositions, aligningPosition):
    diffArray = np.abs(orignalPositions - aligningPosition) 
    return np.sum(diffArray)

def calculateFuelWeighted(orignalPositions, aligningPosition):
    diffArray = np.abs(orignalPositions - aligningPosition)
    weightedDiffArray = [sum(range(diff + 1)) for diff in diffArray]
    return np.sum(weightedDiffArray)

def run7a():
    input = taskHelper.readFile('Data\\data7.txt')[0]
    pattern = r'\d+'
    inputPositions = np.array([int(p) for p in re.findall(pattern, input)])
    numberOfElements = np.shape(inputPositions)[0]
    median = np.median(inputPositions)
    if numberOfElements % 2 == 0:
        totalFuel = calculateFuel(inputPositions, int(median)) 
        print(totalFuel)
    elif numberOfElements % 2 == 1:
        if median % 1 < 0.25: # Median is an integer
            totalFuel = calculateFuel(inputPositions, int(median)) 
            print(totalFuel)
        else:
            totalFuelLower = calculateFuel(inputPositions, round(median))
            totalFuelUpper = calculateFuel(inputPositions, round(median) + 1)
            totalFuel = min(totalFuelLower, totalFuelUpper)
            print(totalFuel)

def run7b():
    input = taskHelper.readFile('Data\\data7.txt')[0]
    pattern = r'\d+'
    inputPositions = np.array([int(p) for p in re.findall(pattern, input)])
    canidateAligners = range(np.amin(inputPositions), np.amax(inputPositions) + 1)
    fuelConsumedPerAligner = [calculateFuelWeighted(inputPositions, aligner) for aligner in canidateAligners]
    totalFuel = min(fuelConsumedPerAligner)
    print(totalFuel)
        

