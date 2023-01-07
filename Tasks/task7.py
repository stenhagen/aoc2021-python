import Helpers.taskHelper as taskHelper
import re
import numpy as np

def calculateFuel(orignalPositions, aligningPosition):
    """ Calculate the fuel spend for aligning all orignalPositions 
    to aligningPosition where all steps cost 1
    """
    diffArray = np.abs(orignalPositions - aligningPosition) 
    return np.sum(diffArray)

def calculateFuelWeighted(orignalPositions, aligningPosition):
    """ Calculate the fuel spend for aligning all orignalPositions 
    to aligningPosition where the step cost increases by the number
    of steps.
    """
    diffArray = np.abs(orignalPositions - aligningPosition)
    weightedDiffArray = [sum(range(diff + 1)) for diff in diffArray]
    return np.sum(weightedDiffArray)

def alignForMinimalFuel(fuelConsumptionFunction):
    input = taskHelper.readFile('Data/data7.txt')[0]
    pattern = r'\d+'
    
    # Extract input positions as np-array of integers.
    inputPositions = np.array([int(p) for p in re.findall(pattern, input)])
    
    # Potential alignment positions is within the range of smallest 
    # and largest value in original set of positions
    canidateAligners =\
        range(np.amin(inputPositions), np.amax(inputPositions) + 1)

    # Calculate fuel spend for all possible alignment positions.
    fuelConsumedPerAligner = [
        fuelConsumptionFunction(inputPositions, aligner)\
        for aligner in canidateAligners
    ]
    # return smallest fuelSpend
    return min(fuelConsumedPerAligner)
    

def run7a():
    totalFuel = alignForMinimalFuel(calculateFuel)
    print(totalFuel)

def run7b():
    totalFuel = alignForMinimalFuel(calculateFuelWeighted)
    print(totalFuel)