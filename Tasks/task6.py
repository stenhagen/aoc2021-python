import Helpers.taskHelper as taskHelper

"""In this task the only difference between part a and b is the 
numberOfDays parameter. As time complexity plays a big role here
the b-part will quickly show inefficiencies if the time complexity
is not capped. So it did for me...

But the final soultion empolyed below does alright 
"""


def getFullReproduction(initialReproductionTime, numberOfDays, startValue, restartValue):
    reproductionSchema = [initialReproductionTime]
    for day in range(numberOfDays):
        newReproductionSchema = []
        numberOfNewFish = 0
        for fish in reproductionSchema:
            if fish > 0:
                newReproductionSchema.append(fish - 1)
            else:
                newReproductionSchema.append(restartValue)
                numberOfNewFish +=1
        newReproductionSchemaWithNewFish = newReproductionSchema + [startValue] * numberOfNewFish
        reproductionSchema = newReproductionSchemaWithNewFish
    return len(reproductionSchema)

def calculatePopulation(numberOfDays):   
    data = taskHelper.readFile('Data/data6.txt')
    startValue = 8
    restartValue = 6
    reproductionSchema = [int(d) for d in data[0].split(',')]
    
    # Throwing exception for cases that are not a possibility given the
    # current input conditions and which might produce unexpected 
    # results  
    try:
        if max(
                max(reproductionSchema), startValue, restartValue
            ) != startValue :
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Solution not implemented for startValue smaller than\
             restartValue or initial values larger than startValue")
        return 

    # Solving by creating buckets of number of fish in each timer value
    # bucket at a day. The outer loop is over number of days and the 
    # inner loop is over range of possible timer values 
    # (0, 1, 2 , ..., startValue). The algorithm is therefore O(n)
    # as number of days scale.

    # Create range of possible timer values
    reproductionValues = range(startValue + 1)
    # Create initial buckets
    reproductionBuckets = [
        reproductionSchema.count(initial) for initial in reproductionValues
    ]
    
    for _ in range(1, numberOfDays + 1):
        # Create new empty buckets.
        newReproductionBuckets = [0] * (startValue + 1)  
        # Loop through possible timer values and fill the corresponding
        # bucket. Note that inside the outer loop we are working with
        # day d but the reproductionBuckets is the result at end of
        # day d-1 and newReproductionBuckets the result at end of
        # day d. The inner loop therefore does not loop over the bucket
        # values of reproductionBuckets but the values of
        # newReproductionBuckets.         
        for v in reproductionValues:
            if v != restartValue and v != startValue:
                newReproductionBuckets[v] = reproductionBuckets[v + 1]
            elif v == restartValue:   
                newReproductionBuckets[v] =\
                    reproductionBuckets[0] + reproductionBuckets[v + 1]
            elif v == startValue:
                newReproductionBuckets[v] = reproductionBuckets[0]
        reproductionBuckets = newReproductionBuckets 
    totalFishAtEnd = sum(reproductionBuckets)
    return totalFishAtEnd
    
def run6a():
    numberOfDays = 80
    finalPopulation = calculatePopulation(numberOfDays)
    print(finalPopulation)

def run6b():
    numberOfDays = 256
    finalPopulation = calculatePopulation(numberOfDays)
    print(finalPopulation)
