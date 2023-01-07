import Helpers.taskHelper as taskHelper

def run1a(): 
    depthMeasurements_str = taskHelper.readFile('Data/data1.txt')

    # Convert list of string to integers   
    depthMeasurements = list(map(lambda s: int(s), depthMeasurements_str))
    
    # Should be solved without increment, through recursion or zipping
    # two copies of depthMeasurements with one position of shift.    
    increasingCounter = 0  
    for idx, depth in enumerate(depthMeasurements[1:]):
        if depth > depthMeasurements[idx]:
            increasingCounter += 1
    
    print(increasingCounter)        
        
def run1b():
    def getSum(l, idx):
        return sum(l[idx : idx + 3])

    depthMeasurements_str = taskHelper.readFile('Data/data1.txt')
    depthMeasurements = list(map(lambda s: int(s), depthMeasurements_str))
    increasingCounter = 0
    for idx, depth in enumerate(depthMeasurements[0:-2]):
        if idx > 0 and getSum(depthMeasurements, idx) > getSum(depthMeasurements, idx - 1):
            increasingCounter += 1
    print(increasingCounter)
