import Helpers.taskHelper as taskHelper

openCloseMap = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<':'>'
}
openSet = set(openCloseMap.keys())
closeSet = set(openCloseMap.values())

def evaluateLineCorruption(line, position, openSequence):
    """ Line corruption detection is solved recursively by keeping a 
    string of the current openings (openSequence) in the order of 
    occurence and stepping forward through the positions in the line. 
    """

    if position >= len(line):
        return ''

    ch = line[position] 
    try:

        # If a new opening is detected it is added to the back of 
        # string.
        if ch in openSet:
            newOpenSequence = openSequence + ch
            return evaluateLineCorruption(
                line, 
                position + 1, 
                newOpenSequence
            )
        if ch in closeSet:
            lastOpenCh = openSequence[-1]
            
            # If a closing matching the last opening is detected, the
            # opening gets removed from the opening sequence.   
            if openCloseMap[lastOpenCh] == ch:
                newOpenSequence = openSequence[:-1]
                return evaluateLineCorruption(
                    line, 
                    position + 1, 
                    newOpenSequence
                )
            
            # If a closing that doesn't match the last opening is
            # opening, there is corruption and the closing is returned
            else:
                return ch
        else:
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Non-valid character") 


def run10a():
    corruptingCharacterPoints = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    rawLines = taskHelper.readFile('Data/data10.txt')
    lines = [line.strip() for line in rawLines]
    
    # Evalute all lines for corruption   
    linesEvaluated = [evaluateLineCorruption(line, 0, '') for line in lines]
    # Get points for corrupted lines
    corruptedPoints = [
        corruptingCharacterPoints[line] 
        for line in linesEvaluated if len(line) > 0
    ]
    corruptionResult = sum(corruptedPoints) # Evaluate result
    print(corruptionResult)


def getIncompleteRemainder(line, position, openSequence):
    """ getIncompleteRemainder returns the remainder of incomplete
    lines. It will fail for corrupted lines 
    """

    # If the full string has been gone through return openSequence 
    if position >= len(line):
        return openSequence  

    ch = line[position]
    try:

        # If a new opening is detected it is added to the back of 
        # string.
        if ch in openSet:
            newOpenSequence = openSequence + ch
            return getIncompleteRemainder(
                line, 
                position + 1, 
                newOpenSequence
            )
        elif ch in closeSet:
            lastOpenCh = openSequence[-1]
            
            try:
                # If a closing matching the last opening is detected, the
                # opening gets removed from the opening sequence.   
                if openCloseMap[lastOpenCh] == ch:
                    newOpenSequence = openSequence[:-1]
                    return getIncompleteRemainder(
                        line, 
                        position + 1, 
                        newOpenSequence
                    )
                
                # If a closing that doesn't match the last opening is
                # opening, there is corruption. Throw exception!
                else:
                    raise(taskHelper.Exc)
            except taskHelper.Exc:
                print("function getShortestClosing() \
                    cannot handle corrupted string")
        else:
            raise(taskHelper.Exc)
    except taskHelper.Exc:
        print("Non-valid character")           


def getShortestClosing(openingSequence):
    """ getShortestClosing takes in a openingSequence, and outputs the
    correspondig closing  
    """
    openingReversed = openingSequence[-1::-1]
    closing = ''.join([openCloseMap[openCh] for openCh in openingReversed])
    return closing


def calculateIncompletePoints(closing):
    closingPoints = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    def incompletePointsRecursive(sequence, points):
        if sequence == '': 
            return points
        else:
            ch = sequence[0]
            newSequence = sequence[1:]
            newPoints = points * 5 + closingPoints[ch]
            return incompletePointsRecursive(newSequence, newPoints)

    return incompletePointsRecursive(closing, 0)

def run10b():
    rawLines = taskHelper.readFile('Data/data10Help.txt')
    lines = [line.strip() for line in rawLines]

    # Get all incomplete (non-corrupted) lines   
    incompleteLines = [
        line for line in lines if evaluateLineCorruption(line, 0, '') == ''
    ]
    
    closings = [
        getShortestClosing(getIncompleteRemainder(line, 0, '')) 
        for line in incompleteLines
    ]

    closingPoints = [calculateIncompletePoints(closing) for closing in closings]

    total = sum(closingPoints)
    print(total)

