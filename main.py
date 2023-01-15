import re
import Helpers.mainHelper as mainHelper

def main() -> int:
    """Echo the input arguments to standard output"""
    print("Welcome to Advent Of Code 2021!")
    taskIdentifier = '0a'
    pattern = r'\d{1,2}[ab]'
    continueRunning = True
    while continueRunning != None:
        taskIdentifier = input("What task would you like to run.\
            Examples: 4a, 12b. End session by some other string: ")
        continueRunning = re.fullmatch(pattern, taskIdentifier)
        if not(continueRunning):
            print("Bye Bye!")
            continue

        if not(mainHelper.taskExists(taskIdentifier)):
            print("The chosen task does not exist")
            continue

        mainHelper.getTask(taskIdentifier)()

if __name__ == '__main__':
    main()