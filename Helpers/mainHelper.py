import Tasks.task1 as task1
import Tasks.task2 as task2
import Tasks.task3 as task3
import Tasks.task4 as task4
import Tasks.task5 as task5
import Tasks.task6 as task6
import Tasks.task7 as task7
import Tasks.task8 as task8


tasks = {
    "1a": task1.run1a,
    "1b": task1.run1b,
    "2a": task2.run2a,
    "2b": task2.run2b,
    "3a": task3.run3a,
    "3b": task3.run3b,
    "4a": task4.run4a,
    "4b": task4.run4b,
    "5a": task5.run5a,
    "5b": task5.run5b,
    "6a": task6.run6a,
    "6b": task6.run6b,
    "7a": task7.run7a,
    "7b": task7.run7b,
    "8a": task8.run8a,
    "8b": task8.run8b
}

def taskExists(k):
    return tasks.get(k) != None

def getTask(k):
    return tasks.get(k)
