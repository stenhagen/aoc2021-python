import Helpers.taskHelper as taskHelper
import re

def interpretCommand(s):
    pattern = r'(?P<command>\w+)\s(?P<steps>\d+)'
    match = re.search(pattern, s)
    commandDictionary = match.groupdict()
    return commandDictionary

def setNewPosition_a(currentPosition, commandStep):
    match commandStep['command']:
        case 'forward': currentPosition['horizontal'] = currentPosition['horizontal'] + int(commandStep['steps']) 
        case 'up': currentPosition['vertical'] = currentPosition['vertical'] - int(commandStep['steps'])
        case 'down': currentPosition['vertical'] = currentPosition['vertical'] + int(commandStep['steps'])
    return currentPosition

def run2a(): 
    commandsRaw = taskHelper.readFile('Data/data2.txt')
    commandSteps = list(map(interpretCommand, commandsRaw))
    position = {'horizontal': 0, 'vertical': 0}
    for cmd in commandSteps:
        position = setNewPosition_a(position, cmd)
    result = position['horizontal'] * position['vertical']
    print(result)

def setNewPosition_b(currentPosition, commandStep):
    match commandStep['command']:
        case 'forward':
            currentPosition['horizontal'] = currentPosition['horizontal'] + int(commandStep['steps'])
            currentPosition['vertical'] = currentPosition['vertical'] + currentPosition['aim'] * int(commandStep['steps'])
        case 'up': 
            currentPosition['aim'] = currentPosition['aim'] - int(commandStep['steps'])
        case 'down':
            currentPosition['aim'] = currentPosition['aim'] + int(commandStep['steps'])
    return currentPosition

def run2b():
    commandsRaw = taskHelper.readFile('Data/data2.txt')
    commandSteps = list(map(interpretCommand, commandsRaw))
    position = {'horizontal': 0, 'vertical': 0, 'aim': 0}
    for cmd in commandSteps:
        position = setNewPosition_b(position, cmd)
    result = position['horizontal'] * position['vertical']
    print(result)