from turtle import position
import Helpers.taskHelper as taskHelper
import numpy as np
import re

"""This tasks works with bingo boards that are three dimensional numpy
matrices. The first two dimensions are the bingo boards. The third 
dimension is a binary number indicating whether the corresponding the
number has been called. Consequently all boards are initialized
with 0s in the third dimension.  
"""

def createBoard(boardString):
    boardRows_str = boardString.split("\n")
    spacePattern = r'\s{1,2}'

    # I get that the for-loop-way of mapping is pythonian and simple 
    # in principal, but it gets nested and ugly fast...   
    boardMatrix_int = [
        [[int(s), 0] for s in re.split(spacePattern, row.strip())] 
        for row in boardRows_str
    ]   
    return np.array(boardMatrix_int)

def crossOffNumber(board, number):
    """Set the flag in the third board-dimension to 1 if the number is
    drawn
    """
    position = np.where(board[:,:,0] == number)
    if len(position[0]) > 0: 
        board[position[0], position[1], 1] = 1 
    return board

def evaluateBoard(board):
    """If a board has all 1s in any row or column it has bingo"""
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
    input = taskHelper.readFile("Data/data4.txt")
    
    # Convert input lines to single string
    inputAsFullString = ''.join(line for line in input)

    # Split to get draw sequence and individual boards. 
    splits = inputAsFullString.split("\n\n") 
    drawString = splits[0] # First item in splits is the draw sequence
    draws_str = drawString.split(',')
    draws_int = [int(d) for d in draws_str] # List of integer draw sequence  
    boardStrings = splits[1:] # Rest of items in splits are boards
    boards = [createBoard(b) for b in boardStrings]
    result = -1

    # Loop through the draw sequence and boards. Cross the drawed number
    # off the board, evaluate if it has bingo and calculate result of the 
    # winning board  
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
    input = taskHelper.readFile("Data/data4.txt")
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


    
    