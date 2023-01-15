import Helpers.taskHelper as taskHelper
import numpy as np
import scipy.signal as signal

def findLowPoints(heightmap):
    """Finds low points
    
    """

    # As filters are flipped in convolution, create them backwards, 
    # e.g. lefFilter = [0, 1, -1] will be applied as [-1, 1, 0] and will
    # find all positions where the value is smaller than the one to its
    # left. The zero should always be added to center the filter with a
    # 1. 
    leftFilter = np.array([[0, 1, -1]])
    rightFilter = np.array([[-1, 1, 0]])
    upFilter = np.array([[0], [1], [-1]])
    downFilter = np.array([[-1], [1], [0]])
    directionFilters = [
        leftFilter, rightFilter, upFilter, downFilter
    ]
    
    # For all filter directions low points are negative produce a list
    # of such maps.
    # mode = 'same' means output has same dimensions as heightmap
    # boundary = 'fill' means pad with fillvalue  
    shiftDifferencePerDirection = [
        signal.convolve2d(
            heightmap, 
            filter, 
            mode = 'same', 
            boundary = 'fill', 
            fillvalue = np.amax(heightmap) + 1
        ) 
        for filter in directionFilters
    ]
    
    # Create binary lowpoint maps and merge them in 3D-numpy matrix
    lowPointsPerDirection = np.array([
        (diffMap < 0).astype(int) 
        for diffMap in shiftDifferencePerDirection
    ])

    # Find points being lowpoints in all direction
    lowPointMap = np.prod(lowPointsPerDirection, axis = 0)
    return lowPointMap

def run9a():
    """ Solved by applying convolution in all 4 directions and finding 
    positions that are low points in all of them.
    """

    lines = taskHelper.readFile('Data/data9.txt')
    heightmap = np.array(
        [[int(pos) for pos in line.strip()] for line in lines]
    )
    lowPointMap = findLowPoints(heightmap)
    # Calculate risk level map  
    lowPointMapRiskLevels = lowPointMap * (heightmap + 1)
    sumOfRiskLevels = np.sum(lowPointMapRiskLevels)
    print(sumOfRiskLevels)


def createLowPointMap(shape, lowPoint):
    """ create low point map with shape = shape
    where lowPoint is the only non-zero element.
    """
    
    zeros = np.zeros(shape, dtype = int)
    zeros[lowPoint[0], lowPoint[1]] = 1
    return zeros


def findFinalBasinSize(basinMap, globalBasinMap):
    """ Recursive algorithm for finding the final basin size for a
    low point and globalBsinMap.

    it works by applying a cross-filter (neighborFilter). Points that
    are part of globalBsinMap and that get a hit in the convolution
    with neighborFilter are part of the basin and gets carried to the
    next recursive iteration as the new basin map.

    Recursion ends when size of input and output basin map are the same.     
    """

    basinSize = np.sum(basinMap)
    neighborFilter = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]
    )
    flowingNeighbors = signal.convolve2d(
        basinMap, 
        neighborFilter, 
        mode = 'same', 
        boundary = 'fill', 
        fillvalue = 0
    )
    flowingNeighborsBinary = (flowingNeighbors > 0).astype(int)
    flowingNeighborsThatFlows = flowingNeighborsBinary * globalBasinMap
    newBasinSize = np.sum(flowingNeighborsThatFlows)
    
    try:
        if newBasinSize > basinSize:
            return findFinalBasinSize(flowingNeighborsThatFlows, globalBasinMap)
        elif newBasinSize == basinSize:
            return basinSize
        else:
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Something is wrong, basinMap cannot shrink in size")
     

def run9b():
    """ Works by applying the recursive alogrithm in findFinalBasinSize.
    """

    lines = taskHelper.readFile('Data/data9.txt')
    heightmap = np.array(
        [[int(pos) for pos in line.strip()] for line in lines]
    )
    # get the low points 
    lowPointMap = findLowPoints(heightmap)

    # Create separate maps for each lowpoint, where the lowpoint is the
    # only non-zero element
    lowPointArrays = np.where(lowPointMap > 0)
    lowPointsList = list(zip(lowPointArrays[0], lowPointArrays[1]))     
    lowPointMaps = [
        createLowPointMap(heightmap.shape, lp) for lp in lowPointsList
    ]

    # Get map of all points that are part of a basin. This was given by 
    # instructions as all points that are not 9. 
    globalBasinMap = (heightmap < 9).astype(int)

    # Calculate the basin sizes for all corresponding low points.
    basinSizesSorted = [
        findFinalBasinSize(lpMap, globalBasinMap) for lpMap in lowPointMaps
    ]
    basinSizesSorted.sort()

    # Calculate the result
    max3basinSizes = np.array(basinSizesSorted[-3:])
    result = np.prod(max3basinSizes)

    print(result)
