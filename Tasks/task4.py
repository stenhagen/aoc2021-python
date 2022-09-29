from turtle import position
import Helpers.taskHelper as taskHelper
import numpy as np
import re

def createBoard(boardString):
    boardRows_str = boardString.split("\n")
    spacePattern = r'\s{1,2}'
    boardMatrix_int = [[[int(s), 0] for s in re.split(spacePattern, row.strip())] for row in boardRows_str] # The   
    return np.array(boardMatrix_int)

def crossOffNumber(board, number):
    position = np.where(board[:,:,0] == number)
    if len(position[0]) > 0: 
        board[position[0], position[1], 1] = 1 
    return board

def evaluateBoard(board):
    activationLayer = board[:,:, 1]
    maxInRows = np.amax(np.sum(activationLayer, axis = 1))
    maxInCols = np.amax(np.sum(activationLayer, axis = 0))
    return maxInRows == 5 or maxInCols == 5

def calculateResult(board, lastDraw):
    activationLayer = board[:,:, 1]
    activationLayerFlipped = (activationLayer * -1) + 1
    nonCrossedSum = np.sum(np.multiply(board[:,:,0], activationLayerFlipped))
    return nonCrossedSum * lastDraw

def run4a():
    input = taskHelper.readFile("Data\\data4.txt")
    inputAsFullString = ''.join(line for line in input)
    splits = inputAsFullString.split("\n\n")
    drawString = splits[0]
    draws_str = drawString.split(',')
    draws_int = [int(d) for d in draws_str] 
    boardStrings = splits[1:]
    boards = [createBoard(b) for b in boardStrings]
    result = -1
    for draw in draws_int:
        for idx, board in enumerate(boards):
            b = crossOffNumber(board, draw)
            isBoardFinished = evaluateBoard(board)
            if isBoardFinished:
                result = calculateResult(b, draw)
                break
            else:
                boards[idx] = b
        if isBoardFinished:
            break
    if result == -1:
        print("No board managed to win")
    print(result)

def run4b():
    input = taskHelper.readFile("Data\\data4.txt")
    inputAsFullString = ''.join(line for line in input)
    splits = inputAsFullString.split("\n\n")
    drawString = splits[0]
    draws_str = drawString.split(',')
    draws_int = [int(d) for d in draws_str] 
    boardStrings = splits[1:]
    boards = [createBoard(b) for b in boardStrings]
    remainingBoards = boards
    result = -1
    for draw in draws_int:
        remainingBoardsCrossed = [crossOffNumber(board, draw) for board in remainingBoards]
        remainingBoardsEvaluated = [b for b in remainingBoardsCrossed if not(evaluateBoard(b))] 
        if len(remainingBoardsEvaluated) == 0:
            result = calculateResult(remainingBoardsCrossed[-1], draw)
            break
        else:
            remainingBoards = remainingBoardsEvaluated
    if result == -1:
        print("Multiple boards did never finish")
    print(result)


    
    