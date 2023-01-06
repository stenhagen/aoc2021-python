import Helpers.taskHelper as taskHelper

def run6a():
    data = taskHelper.readFile('Data/data6.txt')
    reproductionSchema = [int(d) for d in data[0].split(',')]
    
    startValue = 8
    restartValue = 6
    numberOfDays = 256

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
    
    print(len(reproductionSchema))

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

def run6b():
    data = taskHelper.readFile('Data/data6.txt')
    reproductionSchema = [int(d) for d in data[0].split(',')]
    startValue = 8
    restartValue = 6
    numberOfDays = 256
    try:
        if max(max(reproductionSchema), startValue, restartValue) != startValue :
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Solution not implemented for startValue smaller than restartValue or initial values larger than startValue")
        return 

    reproductionValues = range(startValue + 1)
    reproductionBuckets = [reproductionSchema.count(initial) for initial in reproductionValues]
    for day in range(numberOfDays):
        newReproductionBuckets = [0] * (startValue + 1) 
        for v in reproductionValues:
            if v != restartValue and v != startValue:
                newReproductionBuckets[v] = reproductionBuckets[v + 1]
            elif v == restartValue:   
                newReproductionBuckets[v] = reproductionBuckets[0] + reproductionBuckets[v + 1]
            elif v == startValue:
                newReproductionBuckets[v] = reproductionBuckets[0]
        reproductionBuckets = newReproductionBuckets 
    totalFishAtEnd = sum(reproductionBuckets)
    print(totalFishAtEnd)