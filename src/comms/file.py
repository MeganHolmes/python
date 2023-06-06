"""Module providing operations on files"""
import csv
import time
import os
from logging import error

def openFile(path, writeAccess):
    """Opens a file and returns the file object"""
    if writeAccess:
        file = open(path, "w", encoding="utf-8")
    else:
        file = open(path, "r", encoding="utf-8")

    return file

def getListFromCSV(path):
    """Opens a CSV file and returns a list of lists"""
    if isFileCSV(path):
        file = openFile(path, False)
        reader = csv.reader(file)
        array = list(reader)

        if len(array) == 0:
            error("Error: No flashcards found")
            return None

        # Remove trailing empty lines
        while array[-1] == []:
            array.pop()

        file.close()
    else:
        print("Error: File is not a CSV file")
        array = []

    return array

def isFileCSV(path):
    """Checks if a file is a CSV file"""
    return path.endswith(".csv")

def updateCellInCSV(path, row, column, value):
    """Updates a cell in a CSV file"""
    if isFileCSV(path):
        startTime = time.perf_counter()

        file = openFile(path, False)
        reader = csv.reader(file)
        array = list(reader)
        file.close()

        array[row][column] = value

        file = openFile(path, True)
        writer = csv.writer(file)
        writer.writerows(array)
        file.close()
        deleteEmptyLines(path)

        # This method is pretty inefficent but is very simple. This check will
        # will alert if it starts becoming a problem
        timeDiff = time.perf_counter() - startTime
        if timeDiff > 0.1:
            print("Updating CSV file took " + str(timeDiff) + "s. Rewite the updateCellInCSV function")
            time.sleep(1)
    else:
        print("Error: File is not a CSV file")

def deleteEmptyLines(path):
    """Deletes empty lines from a file"""
    file = openFile(path, False)
    lines = file.readlines()
    file.close()

    file = openFile(path, True)
    for line in lines:
        if line == "" or line == "\n":
            continue
        else:
            file.write(line)
    file.close()

def extractRawData(path):
    try:
        with open(path, 'r') as file:
            raw_data = file.read()
        return raw_data
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        return None
    except IOError:
        print(f"Error reading file '{path}'.")
        return None

def getFilesInDirectory(directory_path):
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory_path)
            file_list.append(relative_path)
    return file_list
